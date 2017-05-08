import os
# import unittest
from ..context import bioc
from .utils import assert_everything

# class IterparseTests(unittest.TestCase):
#     def setUp(self):
#         self.src = os.path.join(os.path.dirname(__file__), 'everything.xml')
#
#     def test(self):
#         with bioc.iterparse(self.src) as parser:
#             collection = parser.get_collection_info()
#             for document in parser:
#                 collection.add_document(document)
#         self.assertEqual(2, len(collection.documents))


def test_iterparse():
    filename = os.path.join(os.path.dirname(__file__), 'everything.xml')
    with bioc.iterparse(filename) as parser:
        collection = parser.get_collection_info()
        for document in parser:
            collection.add_document(document)
    assert_everything(collection)