from bidso import (Task,
                   iEEG,
                   )

from bidso.utils import find_root

from bidso.files import (file_Json,
                         )

from bidso.directories import (dir_Root,
                               dir_Session,
                               )

from .paths import BIDS_PATH


def test_file_xxx():

    json_file = file_Json(BIDS_PATH / 'sub-bert/ses-day01/func/sub-bert_ses-day01_task-block_run-00_bold.json')
    find_root(json_file.filename)


def test_directories_xxx():
    dir_Root(BIDS_PATH)

    dir_Session(BIDS_PATH / 'sub-bert/ses-day01')


def test_objects_xxx():
    Task(BIDS_PATH / 'sub-bert/ses-day01/func/sub-bert_ses-day01_task-block_run-00_bold.nii.gz')
    iEEG(BIDS_PATH / 'sub-bert/ses-day02/ieeg/sub-bert_ses-day02_task-block_run-00_ieeg.bin')
