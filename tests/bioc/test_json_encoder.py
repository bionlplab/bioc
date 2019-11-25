import tempfile
from pathlib import Path

import pytest

import bioc
from bioc import biocjson
from bioc.biocjson import BioCJsonIterReader, BioCJsonIterWriter
from tests.utils import assert_everything

file = Path(__file__).parent / 'everything.json'


def test_dump():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)
    tmp = tempfile.mktemp()
    with open(tmp, 'w', encoding='utf8') as fp:
        biocjson.dump(collection, fp)
    with open(tmp, encoding='utf8') as fp:
        collection = biocjson.load(fp)
    assert_everything(collection)


def test_dumps():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)
    s = biocjson.dumps(collection)
    collection = biocjson.loads(s)
    assert_everything(collection)


def test_level():
    with pytest.raises(ValueError):
        BioCJsonIterReader('', level=-1)
    with pytest.raises(ValueError):
        BioCJsonIterWriter('', level=-1)

    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    tmp = tempfile.mktemp()
    with pytest.raises(ValueError):
        with BioCJsonIterWriter(tmp, level=bioc.SENTENCE) as writer:
            writer.write(collection.documents[0])

    with pytest.raises(ValueError):
        with BioCJsonIterWriter(tmp, level=bioc.PASSAGE) as writer:
            writer.write(collection.documents[0])

    with pytest.raises(ValueError):
        with BioCJsonIterWriter(tmp, level=bioc.DOCUMENT) as writer:
            writer.write(collection.documents[0].passages[0])
