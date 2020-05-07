# ndx-bipolar-scheme Extension for NWB

Structure for storing the bipolar schema of a recording in an NWB file.

[![PyPI version](https://badge.fury.io/py/ndx-bipolar-scheme.svg)](https://badge.fury.io/py/ndx-bipolar-scheme)
[![codecov](https://codecov.io/gh/catalystneuro/ndx-bipolar-scheme/branch/master/graph/badge.svg)](https://codecov.io/gh/catalystneuro/ndx-bipolar-scheme)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)



![schema schema](https://github.com/catalystneuro/ndx-bipolar-scheme/blob/master/docs/media/bipolar_schematic.png?raw=true)

## python installation
```bash
$ pip install ndx-bipolar-scheme
```

## python usage

```python
from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import DynamicTableRegion
from datetime import datetime
from ndx_bipolar_scheme import BipolarSchemeTable, EcephysExt
from pynwb.ecephys import ElectricalSeries

import numpy as np

nwbfile = NWBFile('description', 'id', datetime.now().astimezone())

device = nwbfile.create_device('device_name')

electrode_group = nwbfile.create_electrode_group('electrode_group',
                                                 'desc', 'loc', device=device)

for i in np.arange(20.):
    nwbfile.add_electrode(i, i, i, np.nan, 'loc', 'filt', electrode_group)

bipolar_scheme_table = BipolarSchemeTable(name='bipolar_scheme_table',
                                          description='desc')

bipolar_scheme_table.add_row(anodes=[0], cathodes=[1])
bipolar_scheme_table.add_row(anodes=[0, 1], cathodes=[2, 3])
bipolar_scheme_table.add_row(anodes=[0, 1], cathodes=[2])

bipolar_scheme_table.anodes.table = nwbfile.electrodes
bipolar_scheme_table.cathodes.table = nwbfile.electrodes

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
ecephys_ext.bipolar_scheme_table = bipolar_scheme_table
nwbfile.add_lab_meta_data(ecephys_ext)

with NWBHDF5IO('test_nwb.nwb', 'w') as io:
    io.write(nwbfile)

with NWBHDF5IO('test_nwb.nwb', 'r', load_namespaces=True) as io:
    nwbfile = io.read()
    print(nwbfile.acquisition['test_ec_series'].electrodes.table['anodes'][2]['x'])
```
