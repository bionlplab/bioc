import tempfile
from pathlib import Path

import bioc
from tests.utils import assert_everything


file = Path(__file__).parent / 'everything.xml'


def test_dump():
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp)
    tmp = tempfile.mktemp()
    with open(tmp, 'w', encoding='utf8') as fp:
        bioc.dump(collection, fp)
    with open(tmp, encoding='utf8') as fp:
        collection = bioc.load(fp)
    assert_everything(collection)


def test_dumps():
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp)
    s = bioc.dumps(collection)
    collection = bioc.loads(s)
    assert_everything(collection)


def test_BioCXMLDocumentWriter():
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp)

    tmp = tempfile.mktemp()
    with bioc.BioCXMLDocumentWriter(tmp) as writer:
        writer.write_collection_info(collection)
        for document in collection.documents:
            writer.write_document(document)

    with open(tmp, encoding='utf8') as fp:
        collection = bioc.load(fp)

    assert_everything(collection)
