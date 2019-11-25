import json
import tempfile
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
        fromJSON(None, level=5)

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

    tmp = tempfile.mktemp()
    with BioCJsonIterWriter(tmp, level=bioc.DOCUMENT) as writer:
        for doc in collection.documents:
            writer.write(doc)

    del collection.documents[:]
    with pytest.raises(IndexError):
        assert_everything(collection)

    with BioCJsonIterReader(tmp, level=bioc.DOCUMENT) as reader:
        for obj in reader:
            collection.add_document(obj)

    assert_everything(collection)


def test_BioCJsonIterReader_passage():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    tmp = tempfile.mktemp()
    with BioCJsonIterWriter(tmp, level=bioc.PASSAGE) as writer:
        for p in collection.documents[0].passages:
            writer.write(p)

    del collection.documents[0].passages[:]
    with pytest.raises(IndexError):
        assert_everything(collection)

    with BioCJsonIterReader(tmp, level=bioc.PASSAGE) as reader:
        for obj in reader:
            collection.documents[0].add_passage(obj)

    assert_everything(collection)


def test_BioCJsonIterReader_sentence():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    tmp = tempfile.mktemp()
    with BioCJsonIterWriter(tmp, level=bioc.SENTENCE) as writer:
        for s in collection.documents[1].passages[0].sentences:
            writer.write(s)

    del collection.documents[1].passages[0].sentences[:]
    with pytest.raises(IndexError):
        assert_everything(collection)

    with BioCJsonIterReader(tmp, level=bioc.SENTENCE) as reader:
        for obj in reader:
            collection.documents[1].passages[0].add_sentence(obj)

    assert_everything(collection)