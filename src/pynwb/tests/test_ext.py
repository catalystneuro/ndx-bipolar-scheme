import os
from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import DynamicTable, DynamicTableRegion
from datetime import datetime
from ndx_bipolar_scheme import EcephysExt
from pynwb.ecephys import ElectricalSeries
from hdmf.common.table import VectorIndex

import numpy as np
from numpy.testing import assert_array_equal


def test_ext():
    nwbfile = NWBFile('description', 'id', datetime.now().astimezone())

    device = nwbfile.create_device('device_name')

    electrode_group = nwbfile.create_electrode_group('electrode_group',
                                                     'desc', 'loc', device=device)

    for _ in range(20):
        nwbfile.add_electrode(np.nan, np.nan, np.nan, np.nan, 'loc', 'filt',
                              electrode_group)

    anode_electrodes = DynamicTableRegion('anode',
                                          np.arange(0, 20, 2),
                                          'desc',
                                          nwbfile.electrodes)
    cathode_electrodes = DynamicTableRegion('cathode',
                                            np.arange(1, 20, 2),
                                            'desc',
                                            nwbfile.electrodes)

    anode_electrodes_vi = VectorIndex(name='anode_vector_index', data=np.array([0, 3, 8]), target=anode_electrodes)
    cathode_electrodes_vi = VectorIndex(name='cathode_vector_index', data=np.array([0, 1, 3]),
                                        target=cathode_electrodes)

    bipolar_scheme = DynamicTable(name='bipolar_scheme', description='desc', id=np.arange(3))
    bipolar_scheme.add_column(name='anode', description='desc', index=anode_electrodes_vi, table=nwbfile.electrodes)
    bipolar_scheme.add_column(name='cathode', description='desc', index=cathode_electrodes_vi,
                              table=nwbfile.electrodes)

    ecephys_ext = EcephysExt(bipolar_scheme=bipolar_scheme)
    nwbfile.add_lab_meta_data(ecephys_ext)

    bipolar_scheme_region = DynamicTableRegion(
        name='electrodes',
        data=np.arange(0, 3),
        description='desc',
        table=nwbfile.lab_meta_data['extracellular_ephys_extensions'].bipolar_scheme)

    ec_series = ElectricalSeries(name='test_ec_series',
                                 description='desc',
                                 data=np.random.rand(100, 10),
                                 rate=1000.,
                                 electrodes=bipolar_scheme_region)

    nwbfile.add_acquisition(ec_series)

    with NWBHDF5IO('test_nwb.nwb', 'w') as io:
        io.write(nwbfile)

    with NWBHDF5IO('test_nwb.nwb', 'r', load_namespaces=True) as io:
        nwbfile = io.read()
        assert_array_equal(nwbfile.acquisition['test_ec_series'].electrodes.table['anode'].data,
                           np.arange(0, 20, 2))

    os.remove('test_nwb.nwb')
