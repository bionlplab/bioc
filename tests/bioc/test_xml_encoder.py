import io
import tempfile
from pathlib import Path

import pytest

import bioc
from bioc import biocxml
from tests.utils import assert_everything


def _get_collection():
    file = Path(__file__).parent / 'everything.xml'
    with open(file, encoding='utf8') as fp:
        return bioc.load(fp)


def test_dump():
    collection = _get_collection()
    tmp = tempfile.mktemp()
    with open(tmp, 'w', encoding='utf8') as fp:
        bioc.dump(collection, fp)
    with open(tmp, encoding='utf8') as fp:
        collection = bioc.load(fp)
    assert_everything(collection)


def test_dumps():
    collection = _get_collection()
    s = bioc.dumps(collection)
    collection = bioc.loads(s)
    assert_everything(collection)


def test_iterwrite_file():
    collection = _get_collection()

    tmp = tempfile.mktemp()
    with biocxml.iterwrite(tmp) as writer:
        writer.write_collection_info(collection)
        for document in collection.documents:
            writer.write_document(document)

    with open(tmp, encoding='utf8') as fp:
        collection = bioc.load(fp)

    assert_everything(collection)


def test_iterwrite_io():
    collection = _get_collection()
    f = io.BytesIO()
    with biocxml.iterwrite(f) as writer:
        writer.write_collection_info(collection)
        for document in collection.documents:
            writer.write_document(document)

    collection = bioc.loads(f.getvalue().decode('utf-8'))
    assert_everything(collection)
