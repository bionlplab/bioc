from pathlib import Path

import bioc
from tests.utils import assert_everything


def test_iterparse():
    file = Path(__file__).parent / 'everything.xml'
    with bioc.iterparse(file) as parser:
        collection = parser.get_collection_info()
        for document in parser:
            collection.add_document(document)
    assert_everything(collection)
