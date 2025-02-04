import os
from mkdocs.config import config_options
from mkdocs.config.base import Config as BaseConfig
from mkdocs.plugins import BasePlugin
from mkdocs.commands.serve import LiveReloadServer
from mkdocs.utils import write_file
import sass

OUTPUT_CSS_PATHS = ["assets", "stylesheets", "oreui.min.css"]


class ExtensionConfig(BaseConfig):
    internal_dev_watchdog = config_options.Type(str, default='')


class OreUiExtension(BasePlugin[ExtensionConfig]):
    resolve_assets_root: str
    resolve_site_root: str

    def on_config(self, config: BaseConfig, **kwargs) -> BaseConfig:
        self.resolve_assets_root = (
            os.path.join(os.path.dirname(config['config_file_path']), self.config.internal_dev_watchdog)
            if self.config.internal_dev_watchdog
            else os.path.dirname(os.path.abspath(__file__))
        )
        self.resolve_site_root = config['site_dir']
        config["extra_css"] = ['/'.join(OUTPUT_CSS_PATHS)] + config['extra_css']
        return config

    def on_post_build(self, config, **kwargs) -> None:
        css_path = self.resolve_site(*OUTPUT_CSS_PATHS)
        if not os.path.exists(css_path): self.compile_scss()

    def on_serve(self, server: LiveReloadServer, config, **kwargs):
        if not self.config.internal_dev_watchdog: return
        scss_paths = self.resolve_assets('stylesheets')
        server.watch(scss_paths, self.compile_scss)

    def compile_scss(self):
        sass_input = self.resolve_assets('stylesheets', 'index.scss')
        css_output = self.resolve_site(*OUTPUT_CSS_PATHS)

        compiled_css = sass.compile(filename=sass_input, output_style='compressed')
        write_file(compiled_css.encode('utf-8'), css_output)

    def resolve_assets(self, *paths: str):
        return os.path.join(self.resolve_assets_root, *paths)

    def resolve_site(self, *paths: str):
        return os.path.join(self.resolve_site_root, *paths)
