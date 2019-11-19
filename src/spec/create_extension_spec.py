# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc='An NWB:N extension for storing bipolar referencing schema',
        name='ndx-bipolar-scheme',
        version='0.1.0',
        author=list(map(str.strip, 'Ben Dichter'.split(','))),
        contact=list(map(str.strip, 'ben.dichter@gmail.com'.split(',')))
    )

    for type_name in ('LabMetaData', 'DynamicTableRegion', 'DynamicTable', 'VectorIndex'):
        ns_builder.include_type(type_name, namespace='core')

    ecephys_ext = NWBGroupSpec(name='extracellular_ephys_extensions',
                               neurodata_type_def='EcephysExt',
                               neurodata_type_inc='LabMetaData',
                               doc='Group that holds proposed extracellular electrophysiology extensions.')
    bipolar_reference_scheme = ecephys_ext.add_group(name='bipolar_scheme',
                                                     neurodata_type_inc='DynamicTable',
                                                     doc='Table that holds information about the bilpolar referencing '
                                                         'scheme used')
    bipolar_reference_scheme.add_dataset(name='anodes',
                                         neurodata_type_inc='DynamicTableRegion',
                                         doc='references the electrodes table')
    bipolar_reference_scheme.add_dataset(name='anodes_index',
                                         neurodata_type_inc='VectorIndex',
                                         doc='Index into anodes',
                                         quantity='?')
    bipolar_reference_scheme.add_dataset(name='cathode',
                                         neurodata_type_inc='DynamicTableRegion',
                                         doc='references the electrodes table')

    new_data_types = [ecephys_ext]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
