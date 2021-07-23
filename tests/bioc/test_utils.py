import copy
import tempfile
from pathlib import Path

import pytest

import bioc
# import bioc.utils
from tests.utils import assert_everything

file = Path(__file__).parent / 'everything.xml'
with open(file, encoding='utf8') as fp:
    collection = bioc.load(fp)


def test_get_text():
    assert (0, 'abcdefghijklmnopqrstuvwxyz') == bioc.get_text(collection.documents[0])
    assert (27, 'abcdefg测试Non-ASCII') == bioc.get_text(collection.documents[1].passages[0])
    assert (0, '\n' * 27 + 'abcdefg测试Non-ASCII') == bioc.get_text(collection.documents[1])
    assert (34, '测试Non-ASCII') == bioc.get_text(collection.documents[1].passages[0].sentences[1])

    with pytest.raises(TypeError):
        bioc.get_text('Foo')

    # overlapped text
    with pytest.raises(ValueError):
        c = copy.deepcopy(collection)
        c.documents[1].passages[0].sentences[1].offset -= 10
        bioc.get_text(c.documents[1].passages[0])

    # overlapped text
    with pytest.raises(ValueError):
        c = copy.deepcopy(collection)
        c.documents[1].passages[0].offset = -1
        bioc.get_text(c.documents[1])


def test_pretty_print():
    tmp = tempfile.mktemp()
    bioc.pretty_print(file, tmp)
    with open(tmp, encoding='utf8') as fp:
        collection = bioc.load(fp)
    assert_everything(collection)


def test_shorten_text():
    s = 'a' * 10
    assert bioc.utils.shorten_text(s) == repr(s)

    s = 'a' * 50
    assert bioc.utils.shorten_text(s) == repr('a'*17 + ' ... ' + 'a'*17)
