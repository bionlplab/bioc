import io
import json
from pathlib import Path

import pytest

from bioc import biocjson
from tests.utils import assert_everything

file = Path(__file__).parent / 'everything.json'


def test_load():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)
    assert_everything(collection)


def test_loads():
    with open(file, encoding='utf8') as fp:
        s = fp.read()
    collection = biocjson.loads(s)
    assert_everything(collection)


def test_fromJSON():
    # with pytest.raises(ValueError):
    #     biocjson.fromJSON({}, level=5)

    with open(file, encoding='utf8') as fp:
        obj = json.load(fp)

    d = biocjson.fromJSON(obj['documents'][0], 'BioCDocument')
    assert d.id == '1'

    p = biocjson.fromJSON(obj['documents'][0]['passages'][0], 'BioCPassage')
    assert p.text == 'abcdefghijklmnopqrstuvwxyz'

    s = biocjson.fromJSON(obj['documents'][1]['passages'][0]['sentences'][0],
                          'BioCSentence')
    assert s.offset == 27

    with pytest.raises(KeyError):
        biocjson.fromJSON(obj['documents'][0], None)

    with pytest.raises(KeyError):
        biocjson.fromJSON(obj['documents'][0], 'None')


def test_iterreader_document():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    s = io.StringIO()
    with biocjson.iterwriter(s) as writer:
        for doc in collection.documents:
            writer.write(doc)

    del collection.documents[:]
    with pytest.raises(IndexError):
        assert_everything(collection)

    with biocjson.iterreader(io.StringIO(s.getvalue())) as reader:
        for obj in reader:
            collection.add_document(obj)

    assert_everything(collection)


def test_iterreader_passage():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    s = io.StringIO()
    with biocjson.iterwriter(s) as writer:
        for p in collection.documents[0].passages:
            writer.write(p)

    del collection.documents[0].passages[:]
    with pytest.raises(IndexError):
        assert_everything(collection)

    with biocjson.iterreader(io.StringIO(s.getvalue())) as reader:
        for obj in reader:
            collection.documents[0].add_passage(obj)

    assert_everything(collection)


def test_iterreader_sentence():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    s = io.StringIO()
    with biocjson.iterwriter(s) as writer:
        for sen in collection.documents[1].passages[0].sentences:
            writer.write(sen)

    del collection.documents[1].passages[0].sentences[:]
    with pytest.raises(IndexError):
        assert_everything(collection)

    with biocjson.iterreader(io.StringIO(s.getvalue())) as reader:
        for obj in reader:
            collection.documents[1].passages[0].add_sentence(obj)

    assert_everything(collection)
