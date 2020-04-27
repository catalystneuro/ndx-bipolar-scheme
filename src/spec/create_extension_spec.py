# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBRefSpec, NWBAttributeSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc='An NWB:N extension for storing bipolar schema',
        name='ndx-bipolar-scheme',
        version='0.1.0',
        author=list(map(str.strip, 'Ben Dichter'.split(','))),
        contact=list(map(str.strip, 'ben.dichter@gmail.com'.split(',')))
    )

    for type_name in ('LabMetaData', 'DynamicTableRegion', 'DynamicTable', 'VectorIndex', 'VectorData'):
        ns_builder.include_type(type_name, namespace='core')

    ecephys_ext = NWBGroupSpec(name='extracellular_ephys_extensions',
                               neurodata_type_def='EcephysExt',
                               neurodata_type_inc='LabMetaData',
                               doc='Group that holds proposed extracellular electrophysiology extensions.')
    bipolar_scheme = ecephys_ext.add_group(name='bipolar_scheme',
                                           neurodata_type_def='BipolarScheme',
                                           neurodata_type_inc='DynamicTable',
                                           doc='Table that holds information about the bipolar scheme used')
    bipolar_scheme.add_dataset(name='anodes', neurodata_type_inc='DynamicTableRegion',
                               doc='references the electrodes table', attributes=[NWBAttributeSpec(
                                                            name='anode_vector_index',
                                                            doc='A vector index for the anode',
                                                            dtype=NWBRefSpec('VectorIndex', 'region'),
                                                            required=True)])

    bipolar_scheme.add_dataset(name='cathode', neurodata_type_inc='DynamicTableRegion',
                               doc='references the electrodes table', attributes=[NWBAttributeSpec(
                                                            name='cathode_vector_index',
                                                            doc='A vector index for the cathode',
                                                            dtype=NWBRefSpec('VectorIndex', 'region'),
                                                            required=True)])

    new_data_types = [ecephys_ext]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


    BipolarSchemeTable = NWBGroupSpec(
        doc='type for storing time-varying 3D point clouds',
        neurodata_type_def='PointCloudTable',
        neurodata_type_inc='DynamicTable',
        name='BipolarSchemeTable'
    )

    BipolarSchemeTable.add_dataset(
        name='timestamps',
        neurodata_type_inc='VectorData',
        doc='time of each frame in seconds',
        dims=('num_frames',),
        shape=(None,),
        dtype='float')

    BipolarSchemeTable.add_dataset(
        name='point_cloud',
        neurodata_type_inc='VectorData',
        doc='datapoints locations over time',
        dims=('time', '[x, y, z]'),
        shape=(None, 3),
        dtype='float',
    )

    BipolarSchemeTable.add_dataset(
        name='point_cloud_index',
        neurodata_type_inc='VectorIndex',
        doc='datapoints indices',
        dims=('index',),
        shape=(None,),
    )

    BipolarSchemeTable.add_dataset(
        name='color',
        neurodata_type_inc='VectorData',
        doc='datapoints color',
        dims=('time', '[r, g, b]'),
        shape=(None, 3),
        dtype='float',
        quantity='?'
    )

    BipolarSchemeTable.add_dataset(
        name='color_index',
        neurodata_type_inc='VectorIndex',
        doc='datapoints colors indices',
        dims=('index',),
        shape=(None,),
        quantity='?'
    )

    BipolarSchemeTable.add_attribute(
        name='colnames',
        dims=('num_columns',),
        shape=(None,),
        doc='The names of the columns in this table. This should be used to specify '
            'an order to the columns.',
        default_value=('point_cloud',),
        dtype='text'
    )

    new_data_types = [BipolarSchemeTable]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
