import os

from .utils import assert_everything
from ..context import bioc


def test_iterparse():
    filename = os.path.join(os.path.dirname(__file__), 'everything.xml')
    with bioc.iterparse(filename) as parser:
        collection = parser.get_collection_info()
        for document in parser:
            collection.add_document(document)
    assert_everything(collection)
