import os
import numpy as np
from pynwb.file import DynamicTable, DynamicTableRegion
from pynwb import NWBHDF5IO, NWBFile, get_class, load_namespaces, get_manager
from pynwb.ecephys import ElectricalSeries



# Load the .nwb file

path_to_files = 'C:/Users/Admin/Desktop/Ben Dichter/Chang Lab'
fname_nwb = 'EC9_B53.nwb'
fpath_nwb = os.path.join(path_to_files, fname_nwb)

io = NWBHDF5IO(fpath_nwb, mode='r')
nwb = io.read()


# Load namespace and use the extension

load_namespaces("ndx-bipolar-referencing.namespace.yaml")
EcephysExt = get_class('EcephysExt', 'ndx-bipolar-referencing')

# Create a new nwbfile

nwb_new = NWBFile(session_description=nwb.session_description, 
              identifier=nwb.identifier, 
              session_start_time=nwb.session_start_time,
              experimenter=nwb.experimenter,
              lab=nwb.lab,
              institution=nwb.institution,
              experiment_description=nwb.experiment_description,
              session_id=nwb.session_id,
              electrode_groups=nwb.electrode_groups,
              electrodes=nwb.electrodes,
              epochs=nwb.epochs,
              invalid_times=nwb.invalid_times,
              subject=nwb.subject,
              timestamps_reference_time=nwb.timestamps_reference_time,
              trials=nwb.trials)

nwb_new.devices=nwb.devices
nwb_new.intervals=nwb.intervals


# Create Dynamic Table to store for anode and cathode

anode_electrodes = DynamicTableRegion('anode',
                                      np.arange(0, 256, 2),
                                      'desc',
                                      nwb_new.electrodes)
cathode_electrodes = DynamicTableRegion('cathode',
                                        np.arange(1, 256, 2),
                                        'desc',
                                        nwb_new.electrodes)

bipolar_reference_scheme = DynamicTable(name='bipolar_reference_scheme',
                                        description='desc',
                                        columns=[anode_electrodes,
                                                 cathode_electrodes])

# Use the extension module

ecephys_ext = EcephysExt(bipolar_reference_scheme=bipolar_reference_scheme)
nwb_new.add_lab_meta_data(ecephys_ext)

bipolar_scheme = DynamicTableRegion(
    name='electrodes',
    data=[np.nan],
    description='desc',
    table=nwb_new.lab_meta_data['extracellular_electrophysiology_extensions'].bipolar_reference_scheme)

# Build the acuisition

ec_series = ElectricalSeries(name='ElectricalSeries',
                             description=nwb.acquisition['ElectricalSeries'].description,
                             data=nwb.acquisition['ElectricalSeries'].data,
                             rate=nwb.acquisition['ElectricalSeries'].rate,
                             electrodes=bipolar_scheme,
                             conversion=nwb.acquisition['ElectricalSeries'].conversion,
                             resolution=nwb.acquisition['ElectricalSeries'].resolution,
                             starting_time=nwb.acquisition['ElectricalSeries'].starting_time,
                             comments=nwb.acquisition['ElectricalSeries'].comments)

nwb_new.add_acquisition(ec_series)



