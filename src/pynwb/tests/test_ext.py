import os
from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import DynamicTable, DynamicTableRegion
from datetime import datetime
from ndx_bipolar_scheme import BipolarSchemeTable, EcephysExt
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

    bipolar_scheme_table = BipolarSchemeTable(name='bipolar_scheme_table',
                                          description='desc')
    anodes_row1 = DynamicTableRegion('anodes',[0],'desc',nwbfile.electrodes)
    anodes_row2 = DynamicTableRegion('anodes',[0, 1],'desc',nwbfile.electrodes)
    anodes_row3 = DynamicTableRegion('anodes',[0, 1],'desc',nwbfile.electrodes)
    
    cathodes_row1 = DynamicTableRegion('cathodes',[1],'desc',nwbfile.electrodes)
    cathodes_row2 = DynamicTableRegion('cathodes',[2, 3],'desc',nwbfile.electrodes)
    cathodes_row3 = DynamicTableRegion('cathodes',[2],'desc',nwbfile.electrodes)

    bipolar_scheme_table.add_row(anodes=anodes_row1, cathodes=cathodes_row1)
    bipolar_scheme_table.add_row(anodes=anodes_row2, cathodes=cathodes_row2)
    bipolar_scheme_table.add_row(anodes=anodes_row3, cathodes=cathodes_row3)

    bipolar_scheme_region = DynamicTableRegion(
        name='electrodes',
        data=np.arange(0, 3),
        description='desc',
        table=bipolar_scheme_table)

    ec_series = ElectricalSeries(name='test_ec_series',
                                 description='desc',
                                 data=np.random.rand(100, 3),
                                 rate=1000.,
                                 electrodes=bipolar_scheme_region)

    nwbfile.add_acquisition(ec_series)

    ecephys_ext = EcephysExt(name='ecephys_ext')
    nwbfile.add_lab_meta_data(ecephys_ext)


    with NWBHDF5IO('test_nwb.nwb', 'w') as io:
        io.write(nwbfile)

    with NWBHDF5IO('test_nwb.nwb', 'r', load_namespaces=True) as io:
        nwbfile = io.read()
        assert_array_equal(nwbfile.acquisition['test_ec_series'].electrodes.table['anode'][2]['x'], [0., 1.])

    os.remove('test_nwb.nwb')
