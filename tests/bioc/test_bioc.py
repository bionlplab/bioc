import os
import unittest
import tempfile
import bioc


class BioCTests(unittest.TestCase):
    def setUp(self):
        self.src = os.path.join(os.path.dirname(__file__), 'everything.xml')

    def test_load(self):
        with open(self.src) as fp:
            collection = bioc.load(fp)
        self.__test_collection(collection)

    def test_loads(self):
        with open(self.src) as fp:
            s = fp.read()
        collection = bioc.loads(s)
        self.__test_collection(collection)

    def test_dump(self):
        with open(self.src) as fp:
            collection = bioc.load(fp)
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'w') as fp:
            bioc.dump(collection, fp)
        with open(tmp.name) as fp:
            collection = bioc.load(fp)
        self.__test_collection(collection)

    def test_dumps(self):
        with open(self.src) as fp:
            collection = bioc.load(fp)
        s = bioc.dumps(collection)
        collection = bioc.loads(s)
        self.__test_collection(collection)

    def test_validate(self):
        with open(self.src) as fp:
            collection = bioc.load(fp)
        bioc.validate(collection)

    def __test_collection(self, collection):
        self.assertEqual('source', collection.source)
        self.assertEqual('date', collection.date)
        self.assertEqual('key', collection.key)
        self.assertEqual('collection-infon-value', collection.infons['collection-infon-key'])
        document = collection.documents[0]
        self.assertEqual('1', document.id)
        self.assertEqual('document-infon-value', document.infons['document-infon-key'])
        passage = document.passages[0]
        self.assertEqual(0, passage.offset)
        self.assertEqual('passage-infon-value', passage.infons['passage-infon-key'])
        self.assertEqual('abcdefghijklmnopqrstuvwxyz', passage.text)
        annotation = passage.annotations[0]
        self.assertEqual('1', annotation.id)
        self.assertEqual('annotation-infon-value', annotation.infons['annotation-infon-key'])
        self.assertEqual('bc', annotation.text)
        self.assertEqual(1, annotation.get_total_location().offset)
        self.assertEqual(2, annotation.get_total_location().length)
        annotation = passage.annotations[1]
        self.assertEqual('2', annotation.id)
        self.assertEqual('annotation-infon-value', annotation.infons['annotation-infon-key'])
        self.assertEqual('fg', annotation.text)
        self.assertEqual(5, annotation.get_total_location().offset)
        self.assertEqual(2, annotation.get_total_location().length)
        relation = passage.relations[0]
        self.assertEqual('R1', relation.id)
        self.assertEqual('relation-infon-value', relation.infons['relation-infon-key'])
        self.assertEqual('1', relation.nodes[0].refid)
        self.assertEqual('role1', relation.nodes[0].role)
        self.assertEqual('2', relation.nodes[1].refid)
        self.assertEqual('role2', relation.nodes[1].role)
        relation = document.relations[0]
        self.assertEqual('R2', relation.id)
        self.assertEqual('relation-infon-value', relation.infons['relation-infon-key'])
        self.assertEqual('1', relation.nodes[0].refid)
        self.assertEqual('role1', relation.nodes[0].role)
        self.assertEqual('2', relation.nodes[1].refid)
        self.assertEqual('role2', relation.nodes[1].role)

        document = collection.documents[1]
        passage = document.passages[0]
        self.assertEqual(27, passage.offset)
        sentence = passage.sentences[0]
        self.assertEqual(27, sentence.offset)
        self.assertEqual('sentence-infon-value', sentence.infons['sentence-infon-key'])
        self.assertEqual('abcdefg', sentence.text)
        sentence = passage.sentences[1]
        self.assertEqual(34, sentence.offset)
        self.assertEqual('sentence-infon-value', sentence.infons['sentence-infon-key'])
        self.assertEqual('hijklm', sentence.text)
        annotation = passage.sentences[0].annotations[0]
        self.assertEqual('3', annotation.id)
        self.assertEqual('annotation-infon-value', annotation.infons['annotation-infon-key'])
        self.assertEqual('bc', annotation.text)
        self.assertEqual(28, annotation.get_total_location().offset)
        self.assertEqual(2, annotation.get_total_location().length)
        annotation = passage.sentences[1].annotations[0]
        self.assertEqual('4', annotation.id)
        self.assertEqual('annotation-infon-value', annotation.infons['annotation-infon-key'])
        self.assertEqual('hi', annotation.text)
        self.assertEqual(34, annotation.get_total_location().offset)
        self.assertEqual(2, annotation.get_total_location().length)
        relation = passage.sentences[0].relations[0]
        self.assertEqual('R3', relation.id)
        self.assertEqual('relation-infon-value', relation.infons['relation-infon-key'])
        self.assertEqual('3', relation.nodes[0].refid)
        self.assertEqual('role1', relation.nodes[0].role)


if __name__ == '__main__':
    unittest.main()