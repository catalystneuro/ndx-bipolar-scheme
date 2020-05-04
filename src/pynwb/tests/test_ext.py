import os
from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import DynamicTable, DynamicTableRegion
from datetime import datetime
from ndx_bipolar_scheme import BipolarSchemeTable
from pynwb.ecephys import ElectricalSeries

import numpy as np
from numpy.testing import assert_array_equal


def test_ext():
    nwbfile = NWBFile('description', 'id', datetime.now().astimezone())

    device = nwbfile.create_device('device_name')

    electrode_group = nwbfile.create_electrode_group('electrode_group',
                                                     'desc', 'loc', device=device)

    for i in np.arange(20.):
        nwbfile.add_electrode(i, i, i, np.nan, 'loc', 'filt', electrode_group)

    bipolar_scheme = BipolarSchemeTable(name='bipolar_scheme', description='desc')

    bipolar_scheme.add_row(anodes=[0], cathodes=[1])
    bipolar_scheme.add_row(anodes=[0, 1], cathodes=[2, 3])
    bipolar_scheme.add_row(anodes=[0, 1], cathodes=[2])

    bipolar_mod = nwbfile.create_processing_module('bipolar', 'desc')
    nwbfile.processing['bipolar'].add(bipolar_scheme)


    with NWBHDF5IO('test_nwb.nwb', 'w') as io:
        io.write(nwbfile)

    with NWBHDF5IO('test_nwb.nwb', 'r', load_namespaces=True) as io:
        nwbfile = io.read()
        assert_array_equal(nwbfile.acquisition['test_ec_series'].electrodes.table['anode'][2]['x'], [0., 1.])

    os.remove('test_nwb.nwb')
