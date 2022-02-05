import io
import tempfile
from pathlib import Path

import bioc
from bioc import biocxml
from tests.utils import assert_everything


def _get_collection():
    file = Path(__file__).parent / 'everything_v2.xml'
    with open(file, encoding='utf8') as fp:
        return bioc.load(fp, version=bioc.BioCVersion.V2)


def test_dump():
    collection = _get_collection()
    tmp = tempfile.mktemp()
    with open(tmp, 'w', encoding='utf8') as fp:
        bioc.dump(collection, fp, version=bioc.BioCVersion.V2)
    with open(tmp, encoding='utf8') as fp:
        collection = bioc.load(fp, version=bioc.BioCVersion.V2)
    assert_everything(collection)


def test_dumps():
    collection = _get_collection()
    s = bioc.dumps(collection, version=bioc.BioCVersion.V2)
    collection = bioc.loads(s, version=bioc.BioCVersion.V2)
    assert_everything(collection)


def test_BioCXMLDocumentWriter_io():
    collection = _get_collection()

    f = io.BytesIO()
    writer = bioc.BioCXMLDocumentWriter2(f)
    writer.write_collection_info(collection)
    for document in collection.documents:
        writer.write_document(document)
    writer.close()
    collection = bioc.loads(f.getvalue().decode('utf-8'), version=bioc.BioCVersion.V2)
    assert_everything(collection)


def test_BioCXMLDocumentWriter_file():
    collection = _get_collection()

    tmp = tempfile.mktemp()
    with bioc.BioCXMLDocumentWriter2(tmp) as writer:
        writer.write_collection_info(collection)
        for document in collection.documents:
            writer.write_document(document)

    with open(tmp, encoding='utf8') as fp:
        collection = bioc.load(fp, version=bioc.BioCVersion.V2)

    assert_everything(collection)


def test_iterwrite_file():
    collection = _get_collection()

    tmp = tempfile.mktemp()
    with biocxml.iterwrite(tmp, version=bioc.BioCVersion.V2) as writer:
        writer.write_collection_info(collection)
        for document in collection.documents:
            writer.write_document(document)

    with open(tmp, encoding='utf8') as fp:
        collection = bioc.load(fp, version=bioc.BioCVersion.V2)

    assert_everything(collection)


def test_iterwrite_io():
    collection = _get_collection()
    f = io.BytesIO()
    with biocxml.iterwrite(f, version=bioc.BioCVersion.V2) as writer:
        writer.write_collection_info(collection)
        for document in collection.documents:
            writer.write_document(document)

    collection = bioc.loads(f.getvalue().decode('utf-8'), version=bioc.BioCVersion.V2)
    assert_everything(collection)

