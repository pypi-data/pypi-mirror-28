from json import dump
from numpy import NaN, ones, r_, stack
from numpy.random import random, seed

from nibabel import Nifti1Image

from ..utils import replace_extension


def create_bold(mri, bold_file):
    x = mri.get_data()
    DOWNSAMPLE = 4

    af = mri.affine.copy()
    af[:3, :3] *= DOWNSAMPLE   # TODO: these should be some translation as well

    xm = stack([x[i::DOWNSAMPLE, i::DOWNSAMPLE, i::DOWNSAMPLE] for i in range(DOWNSAMPLE)], axis=-1).mean(axis=-1)
    xm[xm == 0] = NaN

    # TODO: nicer time series
    SHIFT = 3
    bold = (xm[:, :, :, None] + r_[ones(SHIFT), ones(16) * 5, ones(16), ones(16) * 5, ones(16), ones(16) * 5, ones(16 - SHIFT)])

    seed(100)
    bold += random(bold.shape) * 2
    nifti = Nifti1Image(bold.astype('float32'), af)
    nifti.header['pixdim'][4] = 2.   # TR
    nifti.to_filename(str(bold_file))

    json_bold = replace_extension(bold_file, '.json')
    with json_bold.open('w') as f:
        dump({}, f)


def create_events(tsv_file):

    DUR = 32
    with tsv_file.open('w') as f:
        f.write('onset\tduration\ttrial_type\n')
        is_move = True
        for i in range(6):
            trial_type = 'move' if is_move else 'rest'
            is_move = not is_move
            f.write(f'{i * DUR}\t{DUR}\t{trial_type}\n')
