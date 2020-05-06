# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec


def main():

    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc='An NWB:N extension for storing bipolar schema',
        name='ndx-bipolar-scheme',
        version='0.1.0',
        author=list(map(str.strip, 'Ben Dichter'.split(','))),
        contact=list(map(str.strip, 'ben.dichter@gmail.com'.split(',')))
    )

    for type_name in ('LabMetaData', 'DynamicTableRegion', 'DynamicTable', 'VectorIndex'):
        ns_builder.include_type(type_name, namespace='core')

    ecephys_ext = NWBGroupSpec(
        doc='Group that holds proposed extracellular electrophysiology extensions.',
        neurodata_type_def='EcephysExt',
        neurodata_type_inc='LabMetaData',
        default_name='ecephys_ext',
        groups=[NWBGroupSpec(
            name='bipolar_scheme_table',
            neurodata_type_inc='BipolarSchemeTable',
            doc='Bipolar referencing scheme used',
            quantity='?'
        )]
    )

    bipolar_scheme = NWBGroupSpec(
        doc='Table that holds information about the bipolar scheme used',
        neurodata_type_def='BipolarSchemeTable',
        neurodata_type_inc='DynamicTable',
        default_name='bipolar_scheme'
    )

    bipolar_scheme.add_dataset(
        name='anodes',
        neurodata_type_inc='DynamicTableRegion',
        doc='references the electrodes table',
        dims=('num_electrodes',),
        shape=(None,),
        dtype='int'
    )

    bipolar_scheme.add_dataset(
        name='cathodes',
        neurodata_type_inc='DynamicTableRegion',
        doc='references the electrodes table',
        dims=('num_electrodes',),
        shape=(None,),
        dtype='int'
    )

    bipolar_scheme.add_dataset(
        name='anodes_index',
        neurodata_type_inc='VectorIndex',
        doc='Indices for the anode table',
        dims=('num_electrode_grp',),
        shape=(None,)
    )

    bipolar_scheme.add_dataset(
        name='cathodes_index',
        neurodata_type_inc='VectorIndex',
        doc='Indices for the cathode table',
        dims=('num_electrode_grp',),
        shape=(None,)
    )

    new_data_types1 = [ecephys_ext]
    new_data_types2 = [bipolar_scheme]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types1, output_dir)
    export_spec(ns_builder, new_data_types2, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
