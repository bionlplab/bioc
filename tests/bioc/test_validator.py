import copy
from pathlib import Path

import pytest

import bioc

file = Path(__file__).parent / 'everything.xml'
with open(file, encoding='utf8') as fp:
    collection = bioc.load(fp)


def test_validate():
    bioc.validate(collection)

    # mismatching annotation
    with pytest.raises(ValueError):
        c = copy.deepcopy(collection)
        c.documents[0].passages[0].annotations[0].text = 'abc'
        bioc.validate(c)

    # mismatching relation node
    with pytest.raises(ValueError):
        c = copy.deepcopy(collection)
        c.documents[0].passages[0].relations[0].nodes[0].refid = 'abc'
        bioc.validate(c)

    # empty sentence text
    with pytest.raises(ValueError):
        c = copy.deepcopy(collection)
        c.documents[1].passages[0].sentences[0].text = None
        bioc.validate(c)

    # overlapped text
    with pytest.raises(ValueError):
        c = copy.deepcopy(collection)
        c.documents[1].passages[0].sentences[1].offset -= 10
        bioc.validate(c)


def test_onerror():
    def onerror(msg, traceback):
        raise AssertionError()

    c = copy.deepcopy(collection)
    c.documents[0].passages[0].annotations[0].text = 'abc'

    with pytest.raises(ValueError):
        bioc.validate(c)

    with pytest.raises(AssertionError):
        bioc.validate(c, onerror=onerror)