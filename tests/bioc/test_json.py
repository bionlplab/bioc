import tempfile
from pathlib import Path

import pytest

import bioc
from bioc import biocjson
from bioc.biocjson import BioCJsonIterReader, BioCJsonIterWriter
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


def test_document():
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


def test_passage():
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


def test_sentence():
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
