import io
import tempfile
from pathlib import Path

import pytest

import bioc
from bioc import biocjson
from bioc.biocjson import BioCJsonIterWriter
# from bioc import BioCFileType
# from bioc import BioCJsonIterWriter
# from bioc import toJSON
from tests.utils import assert_everything

file = Path(__file__).parent / 'everything.json'


def test_dump(tmp_path):
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    filepath = tmp_path / 'foo.json'
    with open(filepath, 'w', encoding='utf8') as fp:
        biocjson.dump(collection, fp)
    with open(filepath, encoding='utf8') as fp:
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
        BioCJsonIterWriter(io.StringIO(), level=-1)

    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    with pytest.raises(ValueError):
        writer = biocjson.BioCJsonIterWriter(io.StringIO(), level=bioc.SENTENCE)
        writer.write(collection.documents[0])

    with pytest.raises(ValueError):
        writer = BioCJsonIterWriter(io.StringIO(), level=bioc.PASSAGE)
        writer.write(collection.documents[0])

    with pytest.raises(ValueError):
        writer = BioCJsonIterWriter(io.StringIO(), level=bioc.DOCUMENT)
        writer.write(collection.documents[0].passages[0])


def test_toJSON():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)
    obj = biocjson.toJSON(collection)
    assert obj['documents'][0]['id'] == '1'

    with pytest.raises(TypeError):
        biocjson.toJSON({})

