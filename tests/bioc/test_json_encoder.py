from pathlib import Path

import pytest

from bioc import biocjson
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


def test_jsoniterwriter(tmp_path):
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    filepath = tmp_path / 'foo.json'
    with biocjson.iterwriter(filepath) as writer:
        for doc in collection.documents:
            writer.write(doc)

    del collection.documents[:]
    with biocjson.iterreader(filepath) as reader:
        for doc in reader:
            collection.add_document(doc)
    assert_everything(collection)


def test_toJSON():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)
    obj = biocjson.toJSON(collection)
    assert obj['documents'][0]['id'] == '1'

    with pytest.raises(TypeError):
        biocjson.toJSON({})

