import os
import unittest
import tempfile
import bioc


class IterwriteTests(unittest.TestCase):
    def setUp(self):
        self.src = os.path.join(os.path.dirname(__file__), 'everything.xml')

    def test(self):
        with open(self.src) as fp:
            collection = bioc.load(fp)
        tmp = tempfile.NamedTemporaryFile()

        with bioc.iterwrite(tmp.name, collection) as writer:
            for document in collection.documents:
                writer.writedocument(document)

        with open(tmp.name, 'r') as fp:
            print(fp.read())
