import tempfile
import pytest
from pathlib import Path

import bioc
import biocjson
from tests.utils import assert_everything

file = Path(__file__).parent / 'everything.json'


def test_document():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    tmp = tempfile.NamedTemporaryFile()
    with biocjson.iterwrite(tmp.name) as writer:
        for doc in collection.documents:
            writer.write(doc)

    del collection.documents[:]
    with pytest.raises(IndexError):
        assert_everything(collection)

    with biocjson.iterparse(tmp.name) as reader:
        for obj in reader:
            collection.add_document(obj)

    assert_everything(collection)


def test_passage():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    tmp = tempfile.NamedTemporaryFile()
    with biocjson.iterwrite(tmp.name, level=bioc.PASSAGE) as writer:
        for p in collection.documents[0].passages:
            writer.write(p)

    del collection.documents[0].passages[:]
    with pytest.raises(IndexError):
        assert_everything(collection)

    with biocjson.iterparse(tmp.name, level=bioc.PASSAGE) as reader:
        for obj in reader:
            collection.documents[0].add_passage(obj)

    assert_everything(collection)


def test_sentence():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)

    tmp = tempfile.NamedTemporaryFile()
    with biocjson.iterwrite(tmp.name, level=bioc.SENTENCE) as writer:
        for s in collection.documents[1].passages[0].sentences:
            writer.write(s)

    del collection.documents[1].passages[0].sentences[:]
    with pytest.raises(IndexError):
        assert_everything(collection)

    with biocjson.iterparse(tmp.name, level=bioc.SENTENCE) as reader:
        for obj in reader:
            collection.documents[1].passages[0].add_sentence(obj)

    assert_everything(collection)
