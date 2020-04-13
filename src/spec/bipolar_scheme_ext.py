
import numpy as np
import os
from pynwb import NWBHDF5IO
from pynwb.ecephys import ElectricalSeries
from pynwb.file import DynamicTable, DynamicTableRegion
from ndx_bipolar_referencing import EcephysExt


# Load the .nwb file

path_to_files = 'C:/Users/Admin/Desktop/Ben Dichter/Chang Lab'
fname_nwb = 'EC9_B53.nwb'
fpath_nwb = os.path.join(path_to_files, fname_nwb)

io = NWBHDF5IO(fpath_nwb, mode='r')
nwb = io.read()


# Make extensions

anode_electrodes = DynamicTableRegion('anode',
                                      np.arange(0, 256, 2),
                                      'desc',
                                      nwb.electrodes)
cathode_electrodes = DynamicTableRegion('cathode',
                                        np.arange(1, 256, 2),
                                        'desc',
                                        nwb.electrodes)

bipolar_reference_scheme = DynamicTable(name='bipolar_reference_scheme',
                                        description='desc',
                                        columns=[anode_electrodes,
                                                 cathode_electrodes])

ecephys_ext = EcephysExt(bipolar_reference_scheme=bipolar_reference_scheme)
nwb.add_lab_meta_data(ecephys_ext)

bipolar_scheme = DynamicTableRegion(
    name='electrodes',
    data=np.arange(0, 128),
    description='desc',
    table=nwb.lab_meta_data['extracellular_electrophysiology_extensions'].bipolar_reference_scheme)

ec_series = ElectricalSeries(name='ecog_series',
                             description='desc',
                             data=np.random.rand(2890015, 128),
                             rate=3051.7578,
                             electrodes=bipolar_scheme,
                             conversion=0.001,
                             resolution=0.0,
                             starting_time=0.0)

nwb.add_acquisition(ec_series)

with NWBHDF5IO('ext_nwb.nwb', 'w') as io:
    io.write(nwb)

with NWBHDF5IO('ext_nwb.nwb', 'r', load_namespaces=True) as io:
    nwbfile = io.read()
    print(nwbfile.acquisition['ecog_series'].electrodes.table['anode'].data)
