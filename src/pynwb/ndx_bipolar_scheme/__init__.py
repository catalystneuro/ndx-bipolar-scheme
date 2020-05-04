import os

from pynwb import load_namespaces

name = 'ndx-bipolar-scheme'

# Set path of the namespace.yaml file to the expected install location
ndx_bipolar_scheme_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    name + '.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_bipolar_scheme_specpath):
    ndx_bipolar_scheme_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        name + '.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_bipolar_scheme_specpath)

from .bipolar_scheme import EcephysExt, BipolarSchemeTable
