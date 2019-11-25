import io
import json
from pathlib import Path

import pytest
from bioc.biocjson.encoder import BioCJsonIterWriter

from bioc import biocjson

import bioc
from bioc.biocjson.decoder import fromJSON, BioCJsonIterReader
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
    with pytest.raises(ValueError):
        fromJSON({}, level=5)

    with open(file, encoding='utf8') as fp:
        obj = json.load(fp)

    d = fromJSON(obj['documents'][0], bioc.DOCUMENT)
    assert d.id == '1'

    p = fromJSON(obj['documents'][0]['passages'][0], bioc.PASSAGE)
    assert p.text == 'abcdefghijklmnopqrstuvwxyz'

    s = fromJSON(obj['documents'][1]['passages'][0]['sentences'][0], bioc.SENTENCE)
    assert s.offset == 27


def test_BioCJsonIterReader_document():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    s = io.StringIO()
    writer = BioCJsonIterWriter(s, level=bioc.DOCUMENT)
    for doc in collection.documents:
        writer.write(doc)

    del collection.documents[:]
    with pytest.raises(IndexError):
        assert_everything(collection)

    reader = BioCJsonIterReader(io.StringIO(s.getvalue()), level=bioc.DOCUMENT)
    for obj in reader:
        collection.add_document(obj)

    assert_everything(collection)


def test_BioCJsonIterReader_passage():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    s = io.StringIO()
    writer = BioCJsonIterWriter(s, level=bioc.PASSAGE)
    for p in collection.documents[0].passages:
        writer.write(p)

    del collection.documents[0].passages[:]
    with pytest.raises(IndexError):
        assert_everything(collection)

    reader = BioCJsonIterReader(io.StringIO(s.getvalue()), level=bioc.PASSAGE)
    for obj in reader:
        collection.documents[0].add_passage(obj)

    assert_everything(collection)


def test_BioCJsonIterReader_sentence():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    s = io.StringIO()
    writer = BioCJsonIterWriter(s, level=bioc.SENTENCE)
    for sen in collection.documents[1].passages[0].sentences:
        writer.write(sen)

    del collection.documents[1].passages[0].sentences[:]
    with pytest.raises(IndexError):
        assert_everything(collection)

    reader = BioCJsonIterReader(io.StringIO(s.getvalue()), level=bioc.SENTENCE)
    for obj in reader:
        collection.documents[1].passages[0].add_sentence(obj)

    assert_everything(collection)


def test_level():
    with pytest.raises(ValueError):
        BioCJsonIterReader(io.StringIO(), level=-1)