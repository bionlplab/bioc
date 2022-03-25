from pathlib import Path

import pytest

from bioc import biocxml
from tests.utils import assert_everything


file = Path(__file__).parent / 'everything.xml'


def test_load():
    with open(file, encoding='utf8') as fp:
        collection = biocxml.load(fp)
    assert_everything(collection)


def test_file_type():
    with pytest.raises(ValueError):
        biocxml.load(open(file, encoding='utf8'), None)

    with pytest.raises(ValueError):
        biocxml.loads('', None)


def test_loads():
    with open(file, encoding='utf8') as fp:
        s = fp.read()
    collection = biocxml.loads(s)
    assert_everything(collection)


def test_iterparse():
    with biocxml.iterparse(open(file, 'rb')) as reader:
        collection = reader.get_collection_info()
        for document in reader:
            collection.add_document(document)
    assert_everything(collection)

    with biocxml.iterparse(str(file)) as reader:
        collection = reader.get_collection_info()
        for document in reader:
            collection.add_document(document)
    assert_everything(collection)