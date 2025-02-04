import os
from setuptools import setup, find_packages

def read(name):
    with open(os.path.join(os.path.dirname(__file__), name), encoding='utf-8') as file:
        return file.read()

setup(
    name='mkdocs-oreui-extension',
    version='0.0.0',
    description='A Mkdocs theme extension plugin featuring MCBE New More-Modern UI Style, based on mkdocs-material.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Cdm2883',
    author_email='hi@cdms.vip',
    url='https://github.com/Cdm2883/mkdocs-oreui-extension',
    packages=find_packages(include=['mkdocs_oreui_extension', 'mkdocs_oreui_extension.*']),
    license="Apache-2.0",
    keywords=[
        'mkdocs',
        'oreui',
    ],
    classifiers=[
        'Framework :: MkDocs',
        'License :: OSI Approved :: Apache Software License',
    ],
    python_requires='>=3.8',
    install_requires=[
        'mkdocs',
        'mkdocs-material',
        'libsass',
    ],
    entry_points={
        'mkdocs.plugins': [
            'oreui-extension = mkdocs_oreui_extension.plugin:OreUiExtension',
        ]
    },
    include_package_data=True,
    package_data={
        'mkdocs_oreui_extension': [
            'stylesheets/*.scss'
        ]
    },
)
