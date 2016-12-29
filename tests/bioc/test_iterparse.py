import os
import unittest
import bioc


class IterparseTests(unittest.TestCase):
    def setUp(self):
        self.src = os.path.join(os.path.dirname(__file__), 'everything.xml')

    def test(self):
        with bioc.iterparse(self.src) as parser:
            collection = parser.get_collection_info()
            for document in parser:
                collection.add_document(document)
        self.assertEqual(2, len(collection.documents))
