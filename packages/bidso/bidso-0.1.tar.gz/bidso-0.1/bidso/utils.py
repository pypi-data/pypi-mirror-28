from pathlib import Path
from re import search


def read_tsv(filename):
    filename = Path(filename)
    with filename.open() as f:
        hdr = f.readline()
        tsv = []
        for l in f:
            d = {k.strip(): v.strip() for k, v in zip(hdr.split('\t'), l.split('\t'))}
            tsv.append(d)
    return tsv


def replace_extension(filename, suffix):
    if isinstance(filename, str):
        return filename.split('.')[0] + suffix
    else:
        return filename.parent / (filename.name.split('.')[0] + suffix)


def add_underscore(filename, suffix):
    if isinstance(filename, str):
        return filename + '_' + suffix
    else:
        return filename.parent / (filename.name + '_' + suffix)


def replace_underscore(filename, suffix):
    return add_underscore(remove_underscore(filename), suffix)


def remove_underscore(filename):
    if isinstance(filename, str):
        return '_'.join(filename.split('_')[:-1])
    else:
        return filename.parent / ('_'.join(filename.name.split('_')[:-1]))


def find_root(filename, pattern='sub-'):
    """Pattern: 'sub-', 'ses-'"""

    if filename.is_dir() and filename.stem.startswith(pattern):
        return filename
    else:
        return find_root(filename.parent)


def bids_mkdir(base_path, file_bids):

    output_path = base_path / ('sub-' + file_bids.subject)
    output_path.mkdir(exist_ok=True)
    if file_bids.session is not None:  # hasattr for pybids, isnone for bidso
        output_path = output_path / ('ses-' + file_bids.session)
        output_path.mkdir(exist_ok=True)

    output_path = output_path / file_bids.modality
    output_path.mkdir(exist_ok=True)

    return output_path


def _match(filename, pattern):
    m = search(pattern, filename.stem)
    if m is None:
        return m
    else:
        return m.group(1)
