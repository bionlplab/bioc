import io
import tempfile
from pathlib import Path

import pytest

import bioc
from bioc import BioCFileType
from bioc import BioCJsonIterWriter
from bioc import toJSON
from tests.utils import assert_everything

file = Path(__file__).parent / 'everything.json'


def test_dump():
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp, BioCFileType.BIOC_JSON)
    tmp = tempfile.mktemp()
    with open(tmp, 'w', encoding='utf8') as fp:
        bioc.dump(collection, fp, BioCFileType.BIOC_JSON)
    with open(tmp, encoding='utf8') as fp:
        collection = bioc.load(fp, BioCFileType.BIOC_JSON)
    assert_everything(collection)


def test_dumps():
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp, BioCFileType.BIOC_JSON)
    s = bioc.dumps(collection, BioCFileType.BIOC_JSON)
    collection = bioc.loads(s, BioCFileType.BIOC_JSON)
    assert_everything(collection)


def test_level():
    with pytest.raises(ValueError):
        BioCJsonIterWriter(io.StringIO(), level=-1)

    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp, BioCFileType.BIOC_JSON)

    with pytest.raises(ValueError):
        writer = BioCJsonIterWriter(io.StringIO(), level=bioc.SENTENCE)
        writer.write(collection.documents[0])

    with pytest.raises(ValueError):
        writer = BioCJsonIterWriter(io.StringIO(), level=bioc.PASSAGE)
        writer.write(collection.documents[0])

    with pytest.raises(ValueError):
        writer = BioCJsonIterWriter(io.StringIO(), level=bioc.DOCUMENT)
        writer.write(collection.documents[0].passages[0])


def test_toJSON():
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp, BioCFileType.BIOC_JSON)
    obj = toJSON(collection)
    assert obj['documents'][0]['id'] == '1'

    with pytest.raises(TypeError):
        toJSON({})

