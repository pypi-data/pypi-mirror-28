from shutil import copyfile
from json import dump
from pathlib import Path
from numpy import ones, memmap, r_
from numpy.random import seed, random


from ..utils import replace_underscore


DATA_PATH = Path(__file__).resolve().parent / 'data'

sf = 256
dur = 192
EFFECT_SIZE = 3
block_dur = 32
EXTRA_CHANS = ('EOG1', 'EOG2', 'ECG', 'EMG', 'other')


def create_electrodes(output_file):
    electrodes_file = DATA_PATH / 'electrodes.tsv'
    copyfile(electrodes_file, output_file)

    coordframe_file = replace_underscore(output_file, 'coordframe.json')
    with coordframe_file.open('w') as f:
        dump({}, f, indent=' ')


def create_ieeg_data(output_file, n_elec):

    n_chan = n_elec + len(EXTRA_CHANS)

    seed(100)
    t = r_[ones(block_dur * sf) * EFFECT_SIZE, ones(block_dur * sf), ones(block_dur * sf) * EFFECT_SIZE, ones(block_dur * sf), ones(block_dur * sf) * EFFECT_SIZE, ones(block_dur * sf)]
    data = random((n_chan, sf * dur)) * t[None, :]

    dtype = 'float64'
    memshape = (n_chan, sf * dur)
    mem = memmap(str(output_file), dtype, mode='w+', shape=memshape, order='F')
    mem[:, :] = data
    mem.flush()


def create_channels(output_file, elec):
    with output_file.open('w') as f:
        f.write('name\ttype\tsampling_frequency\tunits\tstatus\n')
        for one_elec in elec.electrodes.tsv:
            f.write(f'{one_elec["name"]}\tECoG\t{sf}\tmicroV\tgood\n')

        for chan_name in EXTRA_CHANS:
            f.write(f'{chan_name}\tother\t{sf}\tmicroV\tgood\n')


def create_ieeg_info(output_file):
    dataset_info = {
        "TaskName": "block",
        "Manufacturer": "simulated",
        "TaskDescription": "block design",
        "Instructions": "nothing",
        "InstitutionName": "",
        "InstitutionAddress": "",
        "EEGChannelCount": 0,
        "EOGChannelCount": 0,
        "ECGChannelCount": 0,
        "EMGChannelCount": 0,
        "MiscChannelCount": 0,
        "TriggerChannelCount": 0,
        "PowerLineFrequency": 50,
        "RecordingDuration": dur,
        "RecordingType": "continuous",
        "EpochLength": 0,
        "iEEGSurfChannelCount": 0,
        "iEEGDepthChannelCount": 0,
        "iEEGPlacementScheme": "",
        "iEEGReferenceScheme": ""
    }

    with output_file.open('w') as f:
        dump(dataset_info, f, indent=' ')
