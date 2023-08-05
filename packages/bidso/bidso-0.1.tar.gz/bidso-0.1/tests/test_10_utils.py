from bidso.utils import replace_extension, replace_underscore


def test_replace_extension():
    assert replace_extension('file.txt', '.bin') == 'file.bin'


def test_replace_underscore():
    assert replace_underscore('file_mod.txt', 'dat.txt') == 'file_dat.txt'
