import os
from typing import Any, Dict
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.utils import copy_file, write_file
import sass

css_min_paths = ['stylesheets', 'index.min.css']

class OreUiExtension(BasePlugin):
    def on_config(self, config: config_options.Config, **kwargs) -> Dict[str, Any]:
        config['extra_css'] = ['/'.join(css_min_paths)] + config['extra_css']
        return config

    def on_post_build(self, config: Dict[str, Any], **kwargs) -> None:
        src_path = resolve_path(*css_min_paths)
        dest_path = os.path.join(config["site_dir"], *css_min_paths)
        if not os.path.exists(src_path): compile_scss()
        copy_file(src_path, dest_path)

def compile_scss():
    sass_input = resolve_path('stylesheets', 'index.scss')
    css_output = resolve_path(*css_min_paths)

    compiled_css = sass.compile(filename=sass_input, output_style='compressed'),
    write_file(compiled_css.encode('utf-8'), css_output)

def resolve_path(*paths: str):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *paths)
