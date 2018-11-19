from pathlib import Path

import bioc
from tests.utils import assert_everything


file = Path(__file__).parent / 'everything.xml'


def test_load():
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp)
    assert_everything(collection)


def test_loads():
    with open(file, encoding='utf8') as fp:
        s = fp.read()
    collection = bioc.loads(s)
    assert_everything(collection)


def test_BioCXMLDocumentReader():
    with bioc.BioCXMLDocumentReader(file) as reader:
        collection = reader.get_collection_info()
        for document in reader:
            collection.add_document(document)
    assert_everything(collection)

