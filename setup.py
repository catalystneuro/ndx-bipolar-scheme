# -*- coding: utf-8 -*-

import os
from os import path

from setuptools import setup, find_packages
from shutil import copy2

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup_args = {
    'name': 'ndx-bipolar-scheme',
    'version': '0.3.0',
    'description': 'An NWB extension for storing bipolar scheme',
    'author': 'Ben Dichter, Armin Najarpour, Ryan Ly',
    'author_email': 'ben.dichter@catalystneuro.com',
    'url': 'https://github.com/catalystneuro/ndx-bipolar-scheme',
    'license': 'BSD 3-Clause',
    'long_description': long_description,
    'long_description_content_type': "text/markdown",
    'install_requires': [
        'pynwb>=1.1.2'
    ],
    'packages': find_packages('src/pynwb'),
    'package_dir': {'': 'src/pynwb'},
    'package_data': {'ndx_bipolar_scheme': [
        'spec/ndx-bipolar-scheme.namespace.yaml',
        'spec/ndx-bipolar-scheme.extensions.yaml',
    ]},
    'classifiers': [
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    'zip_safe': False
}


def _copy_spec_files(project_dir):
    ns_path = os.path.join(project_dir, 'spec', 'ndx-bipolar-scheme.namespace.yaml')
    ext_path = os.path.join(project_dir, 'spec', 'ndx-bipolar-scheme.extensions.yaml')

    dst_dir = os.path.join(project_dir, 'src', 'pynwb', 'ndx_bipolar_scheme', 'spec')
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    copy2(ns_path, dst_dir)
    copy2(ext_path, dst_dir)


if __name__ == '__main__':
    _copy_spec_files(os.path.dirname(__file__))
    setup(**setup_args)
