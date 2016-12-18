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
        doc = ET.ElementTree(collection.totree())
        return ET.tostring(doc, pretty_print=self.pretty_print, encoding=collection.encoding,
                           standalone=collection.standalone)

    def totree(self, collection):
        """
        Returns the BioC xml tree that the BioCollection represents as a ElementTree .

        :return: the BioC xml that the BioCollection represents as a ElementTree .
        :rtype: ElementTree
        """
        ctree = ET.Element('collection')
        ET.SubElement(ctree, 'source').text = collection.source
        ET.SubElement(ctree, 'date').text = collection.date
        ET.SubElement(ctree, 'key').text = collection.key
        self.__encode_infons(ctree, collection.infons)

        for d in collection.documents:
            self.__encode_document(ET.SubElement(ctree, 'document'), d)

        return ctree

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
        atree = ET.SubElement(parent, 'annotation', {'id': annotation.id})
        self.__encode_infons(atree, annotation.infons)
        for l in annotation.locations:
            ET.SubElement(atree, 'location', {'offset': str(l.offset), 'length': str(l.length)})
        ET.SubElement(atree, 'text').text = annotation.text

    def __encode_relation(self, parent, relation):
        rtree = ET.SubElement(parent, 'relation', {'id': relation.id})
        self.__encode_infons(rtree, relation.infons)
        for n in relation.nodes:
            ET.SubElement(rtree, 'node', {'refid': n.refid, 'role': n.role})

    def __encode_infons(self, parent, infons):
        for k, v in infons.items():
            ET.SubElement(parent, 'infon', {'key': str(k)}).text = str(v)
