import lxml.etree as ET


class BioCEncoder(object):
    def __init__(self, pretty_print=True):
        """
        Constructor for BioCEncoder, with sensible defaults.

        :param pretty_print: (bool) enables formatted XML
        """
        self.pretty_print = pretty_print

    def encode(self, collection):
        """
        Return a BioC formatted string representation of a BioC collection structure.

        :param collection: a BioC collection
        :return: a BioC formatted ``str``
        """
        doc = ET.ElementTree(self.totree(collection))
        return ET.tostring(doc, pretty_print=self.pretty_print, encoding=collection.encoding,
                           standalone=collection.standalone)

    def totree(self, collection):
        """
        Returns the BioC xml tree that the BioCollection represents as a ElementTree.

        :param collection: a BioC collection
        :return: the BioC xml that the BioCollection represents as a ElementTree.
        :rtype: ElementTree
        """
        tree = ET.Element('collection')
        ET.SubElement(tree, 'source').text = collection.source
        ET.SubElement(tree, 'date').text = collection.date
        ET.SubElement(tree, 'key').text = collection.key
        self.__encode_infons(tree, collection.infons)
        for d in collection.documents:
            self.__encode_document(ET.SubElement(tree, 'document'), d)
        return tree

    def __encode_document(self, dtree, document):
        ET.SubElement(dtree, 'id').text = document.id
        self.__encode_infons(dtree, document.infons)
        for p in document.passages:
            self.__encode_passage(ET.SubElement(dtree, 'passage'), p)
        for a in document.annotations:
            self.__encode_annotation(dtree, a)
        for r in document.relations:
            self.__encode_relation(dtree, r)

    def __encode_passage(self, ptree, passage):
        self.__encode_infons(ptree, passage.infons)
        ET.SubElement(ptree, 'offset').text = str(passage.offset)
        if passage.text:
            ET.SubElement(ptree, 'text').text = passage.text
        for s in passage.sentences:
            self.__encode_sentence(ET.SubElement(ptree, 'sentence'), s)
        for a in passage.annotations:
            self.__encode_annotation(ptree, a)
        for r in passage.relations:
            self.__encode_relation(ptree, r)

    def __encode_sentence(self, stree, sentence):
        self.__encode_infons(stree, sentence.infons)
        ET.SubElement(stree, 'offset').text = str(sentence.offset)
        if sentence.text:
            ET.SubElement(stree, 'text').text = sentence.text
        for a in sentence.annotations:
            self.__encode_annotation(stree, a)
        for r in sentence.relations:
            self.__encode_relation(stree, r)

    def __encode_annotation(self, parent, annotation):
        tree = ET.SubElement(parent, 'annotation', {'id': annotation.id})
        self.__encode_infons(tree, annotation.infons)
        for l in annotation.locations:
            ET.SubElement(tree, 'location', {'offset': str(l.offset), 'length': str(l.length)})
        ET.SubElement(tree, 'text').text = annotation.text

    def __encode_relation(self, parent, relation):
        tree = ET.SubElement(parent, 'relation', {'id': relation.id})
        self.__encode_infons(tree, relation.infons)
        for n in relation.nodes:
            ET.SubElement(tree, 'node', {'refid': n.refid, 'role': n.role})

    def __encode_infons(self, parent, infons):
        for k, v in infons.items():
            ET.SubElement(parent, 'infon', {'key': str(k)}).text = str(v)
