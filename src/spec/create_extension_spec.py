# -*- coding: utf-8 -*-

import os.path

from hdmf.spec import NamespaceBuilder, GroupSpec
from hdmf.spec.write import export_spec


def main():

    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NamespaceBuilder(
        doc='An NWB:N extension for storing bipolar schema',
        name='ndx-bipolar-scheme',
        version='0.1.0',
        author=list(map(str.strip, 'Ben Dichter'.split(','))),
        contact=list(map(str.strip, 'ben.dichter@gmail.com'.split(',')))
    )

    for type_name in ('LabMetaData', 'DynamicTableRegion', 'DynamicTable', 'VectorIndex', 'VectorData'):
        ns_builder.include_type(type_name, namespace='hdmf-common')

    ecephys_ext = GroupSpec(
        doc='Group that holds proposed extracellular electrophysiology extensions.',
        data_type_def='EcephysExt',
        data_type_inc='LabMetaData',
        default_name='ecephys_ext'
    )

    bipolar_scheme = ecephys_ext.add_group(
        name='bipolar_scheme',
        data_type_def='BipolarScheme',
        data_type_inc='DynamicTable',
        doc='Table that holds information about the bipolar scheme used'
    )

    bipolar_scheme.add_dataset(
        name='anodes',
        data_type_inc='DynamicTableRegion',
        doc='references the electrodes table',
        dims=('num_electrode_grp',),
        shape=(None,),
        dtype='int'
    )

    bipolar_scheme.add_dataset(
        name='cathode',
        data_type_inc='DynamicTableRegion',
        doc='references the electrodes table',
        dims=('num_electrode_grp',),
        shape=(None,),
        dtype='int'
    )

    bipolar_scheme.add_dataset(
        name='anodes_vector_index',
        data_type_inc='VectorIndex',
        doc='Indices for the anode table',
        dims=('index',),
        shape=(None,)
    )

    bipolar_scheme.add_dataset(
        name='cathodes_vector_index',
        data_type_inc='VectorIndex',
        doc='Indices for the cathode table',
        dims=('index',),
        shape=(None,)
    )

    new_data_types = [ecephys_ext]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


    BipolarSchemeTable = GroupSpec(
        doc='type for storing time-varying 3D point clouds',
        data_type_def='PointCloudTable',
        data_type_inc='DynamicTable',
        default_name='BipolarSchemeTable'
    )

    BipolarSchemeTable.add_dataset(
        name='timestamps',
        data_type_inc='VectorData',
        doc='time of each frame in seconds',
        dims=('num_frames',),
        shape=(None,),
        dtype='float')

    BipolarSchemeTable.add_dataset(
        name='point_cloud',
        data_type_inc='VectorData',
        doc='datapoints locations over time',
        dims=('time', '[x, y, z]'),
        shape=(None, 3),
        dtype='float',
    )

    BipolarSchemeTable.add_dataset(
        name='point_cloud_index',
        data_type_inc='VectorIndex',
        doc='datapoints indices',
        dims=('index',),
        shape=(None,),
    )

    BipolarSchemeTable.add_dataset(
        name='color',
        data_type_inc='VectorData',
        doc='datapoints color',
        dims=('time', '[r, g, b]'),
        shape=(None, 3),
        dtype='float',
        quantity='?'
    )

    BipolarSchemeTable.add_dataset(
        name='color_index',
        data_type_inc='VectorIndex',
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
