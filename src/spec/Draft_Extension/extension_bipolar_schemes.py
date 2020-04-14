from pynwb.spec import NWBNamespaceBuilder, NWBGroupSpec, export_spec

ns_builder = NWBNamespaceBuilder(
        doc='An NWB:N extension for storing bipolar referencing schema',
        name='ndx-bipolar-referencing',
        version='0.1.0',
        author=list(map(str.strip, 'Ben Dichter'.split(','))),
        contact=list(map(str.strip, 'ben.dichter@gmail.com'.split(',')))
    )


for type_name in ('LabMetaData', 'DynamicTableRegion', 'DynamicTable'):
        ns_builder.include_type(type_name, namespace='core')


ecephys_ext = NWBGroupSpec(name='extracellular_electrophysiology_extensions',
                               neurodata_type_def='EcephysExt',
                               neurodata_type_inc='LabMetaData',
                               doc='Group that holds proposed extracellular electrophysiology extensions.')

bipolar_reference_scheme = ecephys_ext.add_group(name='bipolar_reference_scheme',
                                                 neurodata_type_inc='DynamicTable',
                                                 doc='Table that holds information about the bilpolar referencing '
                                                     'scheme used')
bipolar_reference_scheme.add_dataset(name='anodes',
                                     neurodata_type_inc='DynamicTableRegion',
                                     doc='references the electrodes table')

bipolar_reference_scheme.add_dataset(name='cathode',
                                     neurodata_type_inc='DynamicTableRegion',
                                     doc='references the electrodes table')

new_data_types = [ecephys_ext]

output_dir = 'C:/Users/Admin/Desktop/Ben Dichter/Chang Lab'

export_spec(ns_builder, new_data_types, output_dir)
