import os
import hashlib
from mkdocs.config import config_options
from mkdocs.config.base import Config as BaseConfig
from mkdocs.plugins import BasePlugin
from mkdocs.commands.serve import LiveReloadServer
from mkdocs.utils import write_file
import sass

OUTPUT_CSS_PATHS = ["assets", "stylesheets", "oreui"]


class ExtensionConfig(BaseConfig):
    internal_dev_watchdog = config_options.Type(str, default='')


class OreUiExtension(BasePlugin[ExtensionConfig]):
    resolve_assets_root: str
    resolve_site_root: str
    css_compiled_paths = OUTPUT_CSS_PATHS[:-1] + [OUTPUT_CSS_PATHS[-1] + '.min.css']
    css_compiled: str
    is_serve_mode: bool

    def on_startup(self, command: str, **kwargs):
        self.is_serve_mode = command == 'serve'

    def on_config(self, config: BaseConfig, **kwargs) -> BaseConfig:
        self.resolve_assets_root = (
            os.path.join(os.path.dirname(config['config_file_path']), self.config.internal_dev_watchdog)
            if self.config.internal_dev_watchdog
            else os.path.dirname(os.path.abspath(__file__))
        )
        self.resolve_site_root = config['site_dir']
        self.compile_scss()
        config['extra_css'] = ['/'.join(self.css_compiled_paths)] + config['extra_css']
        return config

    def on_post_build(self, config, **kwargs) -> None:
        self.output_css()

    def on_serve(self, server: LiveReloadServer, config, **kwargs):
        if not self.config.internal_dev_watchdog: return
        scss_paths = self.resolve_assets('stylesheets')
        server.watch(scss_paths, self.internal_dev_watchdog)

    def internal_dev_watchdog(self):
        self.compile_scss()
        self.output_css()

    def compile_scss(self):
        sass_input = self.resolve_assets('stylesheets', 'index.scss')
        self.css_compiled = sass.compile(filename=sass_input, output_style='compressed').encode('utf-8')
        if self.config.internal_dev_watchdog and self.is_serve_mode: return
        file_hash = hashlib.md5(self.css_compiled).hexdigest()[:8]
        self.css_compiled_paths = OUTPUT_CSS_PATHS[:-1] + [OUTPUT_CSS_PATHS[-1] + '.' + file_hash + '.min.css']

    def output_css(self):
        css_output = self.resolve_site(*self.css_compiled_paths)
        write_file(self.css_compiled, css_output)

    def resolve_assets(self, *paths: str):
        return os.path.join(self.resolve_assets_root, *paths)

    def resolve_site(self, *paths: str):
        return os.path.join(self.resolve_site_root, *paths)
