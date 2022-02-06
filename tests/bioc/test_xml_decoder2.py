from pathlib import Path

import bioc
from bioc import biocxml
from tests.utils import assert_everything


file = Path(__file__).parent / 'everything_v2.xml'


def test_load():
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp, version=bioc.BioCVersion.V2)
    assert_everything(collection)


def test_loads():
    with open(file, encoding='utf8') as fp:
        s = fp.read()
    collection = bioc.loads(s, version=bioc.BioCVersion.V2)
    assert_everything(collection)


def test_iterparse():
    with biocxml.iterparse(open(file, 'rb'), version=bioc.BioCVersion.V2) as reader:
        collection = reader.get_collection_info()
        for document in reader:
            collection.add_document(document)
    assert_everything(collection)

    with biocxml.iterparse(str(file), version=bioc.BioCVersion.V2) as reader:
        collection = reader.get_collection_info()
        for document in reader:
            collection.add_document(document)
    assert_everything(collection)
