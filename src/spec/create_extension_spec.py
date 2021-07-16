# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBLinkSpec, NWBDatasetSpec


def main():

    # these arguments were auto-generated from your cookie-cutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc='An NWB extension for storing bipolar schema',
        name='ndx-bipolar-scheme',
        version='0.4.0',
        author=list(map(str.strip, 'Ben Dichter,Armin Najarpour,Ryan Ly'.split(','))),
        contact=list(map(str.strip, 'ben.dichter@catalystneuro.com'.split(',')))
    )

    for type_name in ('LabMetaData', 'DynamicTableRegion', 'DynamicTable', 'VectorIndex', 'ElectricalSeries'):
        ns_builder.include_type(type_name, namespace='core')

    ndx_bipolar_scheme = NWBGroupSpec(
        doc='Group that holds proposed extracellular electrophysiology extensions.',
        neurodata_type_def='NdxBipolarScheme',
        neurodata_type_inc='LabMetaData',
        name='ndx_bipolar_scheme',
        groups=[NWBGroupSpec(
            neurodata_type_inc='BipolarSchemeTable',
            doc='Bipolar referencing scheme used',
            quantity='*'
        )],
        links=[NWBLinkSpec(
            name='source',
            doc='input to re-referencing scheme',
            target_type='ElectricalSeries',
            quantity='?',
        )]
    )

    bipolar_scheme_table = NWBGroupSpec(
        default_name='bipolar_scheme',
        doc='Table that holds information about the bipolar scheme used',
        neurodata_type_def='BipolarSchemeTable',
        neurodata_type_inc='DynamicTable',
        datasets=[
            NWBDatasetSpec(
                name='anodes',
                neurodata_type_inc='DynamicTableRegion',
                doc='references the electrodes table',
                dims=('num_electrodes',),
                shape=(None,),
                dtype='int'
            ),
            NWBDatasetSpec(
                name='cathodes',
                neurodata_type_inc='DynamicTableRegion',
                doc='references the electrodes table',
                dims=('num_electrodes',),
                shape=(None,),
                dtype='int'
            ),
            NWBDatasetSpec(
                name='anodes_index',
                neurodata_type_inc='VectorIndex',
                doc='Indices for the anode table',
                dims=('num_electrode_grp',),
                shape=(None,),
                quantity='?',
            ),
            NWBDatasetSpec(
                name='cathodes_index',
                neurodata_type_inc='VectorIndex',
                doc='Indices for the cathode table',
                dims=('num_electrode_grp',),
                shape=(None,),
                quantity='?',
            )
        ]
    )

    new_data_types = [ndx_bipolar_scheme, bipolar_scheme_table]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
