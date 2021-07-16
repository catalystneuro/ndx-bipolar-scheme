import os
from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import DynamicTableRegion
from datetime import datetime
from ndx_bipolar_scheme import BipolarSchemeTable, NdxBipolarScheme
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

    electrodes = DynamicTableRegion(
        name='electrodes',
        data=np.arange(0, 3),
        description='desc',
        table=nwbfile.electrodes,
    )

    source_ec_series = ElectricalSeries(
        name='source_ec_series',
        description='desc',
        data=np.random.rand(100, 3),
        rate=1000.,
        electrodes=electrodes,
    )

    nwbfile.add_acquisition(source_ec_series)

    bipolar_scheme_table = BipolarSchemeTable(
        name='bipolar_scheme', description='desc'
    )

    bipolar_scheme_table.add_row(anodes=[0], cathodes=[1])
    bipolar_scheme_table.add_row(anodes=[0, 1], cathodes=[2, 3])
    bipolar_scheme_table.add_row(anodes=[0, 1], cathodes=[2])

    bipolar_scheme_table['anodes'].target.table = nwbfile.electrodes
    bipolar_scheme_table['cathodes'].target.table = nwbfile.electrodes

    bipolar_scheme_region = DynamicTableRegion(
        name='electrodes',
        data=np.arange(0, 3),
        description='desc',
        table=bipolar_scheme_table,
    )

    ec_series = ElectricalSeries(
        name='dest_ec_series',
        description='desc',
        data=np.random.rand(100, 3),
        rate=1000.,
        electrodes=bipolar_scheme_region,
    )

    nwbfile.add_acquisition(ec_series)

    ndx_bipolar_scheme = NdxBipolarScheme(bipolar_scheme_tables=[bipolar_scheme_table], source=source_ec_series)
    nwbfile.add_lab_meta_data(ndx_bipolar_scheme)

    with NWBHDF5IO('test_nwb.nwb', 'w') as io:
        io.write(nwbfile)

    with NWBHDF5IO('test_nwb.nwb', 'r', load_namespaces=True) as io:
        nwbfile = io.read()
        assert_array_equal(nwbfile.acquisition['dest_ec_series'].electrodes.table['anodes'][2]['x'], [0., 1.])

    os.remove('test_nwb.nwb')
