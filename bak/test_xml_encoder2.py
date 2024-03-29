import io
import tempfile
from pathlib import Path

import bioc
from bioc import biocxml
from tests.utils import assert_everything


def _get_collection():
    file = Path(__file__).parent / 'everything_v2.xml'
    with open(file, encoding='utf8') as fp:
        return biocxml.load(fp, version=bioc.BioCVersion.V2)


def test_dump():
    collection = _get_collection()
    tmp = tempfile.mktemp()
    with open(tmp, 'w', encoding='utf8') as fp:
        biocxml.dump(collection, fp, version=bioc.BioCVersion.V2)
    with open(tmp, encoding='utf8') as fp:
        collection = biocxml.load(fp, version=bioc.BioCVersion.V2)
    assert_everything(collection)


def test_dumps():
    collection = _get_collection()
    s = biocxml.dumps(collection, version=bioc.BioCVersion.V2)
    collection = biocxml.loads(s, version=bioc.BioCVersion.V2)
    assert_everything(collection)


def test_iterwrite_file():
    collection = _get_collection()

    tmp = tempfile.mktemp()
    with biocxml.iterwrite(tmp, version=bioc.BioCVersion.V2) as writer:
        writer.write_collection_info(collection)
        for document in collection.documents:
            writer.write_document(document)

    with open(tmp, encoding='utf8') as fp:
        collection = biocxml.load(fp, version=bioc.BioCVersion.V2)

    assert_everything(collection)


def test_iterwrite_io():
    collection = _get_collection()
    f = io.BytesIO()
    with biocxml.iterwrite(f, version=bioc.BioCVersion.V2) as writer:
        writer.write_collection_info(collection)
        for document in collection.documents:
            writer.write_document(document)

    collection = biocxml.loads(f.getvalue().decode('utf-8'), version=bioc.BioCVersion.V2)
    assert_everything(collection)

