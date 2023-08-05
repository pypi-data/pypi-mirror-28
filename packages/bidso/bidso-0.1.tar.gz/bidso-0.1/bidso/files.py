from json import load as json_load
from pathlib import Path

from .utils import read_tsv, _match


class file_Core():
    def __init__(self, filename):
        """TODO: maybe it's better to split them based on the file type"""
        self.filename = Path(filename)
        self.subject = _match(self.filename, 'sub-([a-zA-Z0-9\-]+)_')
        self.session = _match(self.filename, '_ses-([a-zA-Z0-9\-]+)_')
        self.modality = self.filename.parent.name
        self.run = _match(self.filename, '_run-([a-zA-Z0-9\-]+)_')
        self.acq = _match(self.filename, '_acq-([a-zA-Z0-9\-]+)_')
        self.task = _match(self.filename, '_task-([a-zA-Z0-9\-]+)_')


class file_Tsv(file_Core):
    def __init__(self, filename):
        super().__init__(filename)
        self.tsv = read_tsv(self.filename)


class file_Json(file_Core):
    def __init__(self, filename):
        super().__init__(filename)
        with self.filename.open() as f:
            self.json = json_load(f)


class file_Channels(file_Tsv):
    def __init__(self, filename):
        super().__init__(filename)


class file_Events(file_Tsv):
    def __init__(self, filename):
        super().__init__(filename)


class file_Electrodes(file_Tsv):
    def __init__(self, filename):
        super().__init__(filename)
