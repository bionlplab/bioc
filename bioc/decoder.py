import lxml.etree as ET

from .bioc import (
    BioCCollection,
    BioCDocument,
    BioCPassage,
    BioCSentence,
    BioCAnnotation,
    BioCRelation,
    BioCLocation,
    BioCNode
)


class BioCDecoder(object):
    def __init__(self):
        pass

    def decode(self, s):
        """
        Deserialize ``s`` to a BioC collection object.
        :param s: a ``str`` instance containing a BioC collection
        :return a object of BioCollection
        """
        tree = ET.fromstring(s)
        collection = self.__parse_collection(tree.getroot())
        collection.encoding = tree.docinfo.encoding
        collection.standalone = tree.docinfo.standalone
        collection.version = tree.docinfo.xml_version
        return collection

    def __parse_collection(self, ctree):
        collection = BioCCollection()
        collection.source = ctree.findtext('source')
        collection.date = ctree.findtext('date')
        collection.key = ctree.findtext('key')
        collection.infons = self.__parse_infons(ctree)

        for dtree in ctree.findall('document'):
            collection.add_document(self.__parse_document(dtree))

        return collection

    def __parse_document(self, dtree):
        document = BioCDocument()
        document.id = dtree.findtext('id')
        document.infons = self.__parse_infons(dtree)

        for ptree in dtree.findall('passage'):
            document.add_passage(self.__parse_passage(ptree))

        for atree in dtree.findall('annotation'):
            document.add_annotation(self.__parse_annotation(atree))

        for rtree in dtree.findall('relation'):
            document.add_relation(self.__parse_relation(rtree))
        return document

    def __parse_passage(self, ptree):
        passage = BioCPassage()
        passage.offset = int(ptree.findtext('offset'))
        passage.infons = self.__parse_infons(ptree)
        if ptree.find('text') is not None:
            passage.text = ptree.findtext('text')

        for stree in ptree.findall('sentence'):
            passage.add_sentence(self.__parse_sentence(stree))

        for atree in ptree.findall('annotation'):
            passage.add_annotation(self.__parse_annotation(atree))

        for rtree in ptree.findall('relation'):
            passage.add_relation(self.__parse_relation(rtree))

        return passage

    def __parse_sentence(self, stree):
        sentence = BioCSentence()
        sentence.offset = int(stree.findtext('offset'))
        sentence.text = stree.findtext('text')
        sentence.infons = self.__parse_infons(stree)

        for atree in stree.findall('annotation'):
            sentence.add_annotation(self.__parse_annotation(atree))

        for rtree in stree.findall('relation'):
            sentence.add_relation(self.__parse_relation(rtree))

        return sentence

    def __parse_annotation(self, atree):
        annotation = BioCAnnotation()
        annotation.id = atree.attrib['id']
        annotation.infons = self.__parse_infons(atree)
        annotation.text = atree.findtext('text')
        for ltree in atree.findall('location'):
            annotation.add_location(
                BioCLocation(int(ltree.attrib['offset']), int(ltree.attrib['length'])))
        return annotation

    def __parse_relation(self, rtree):
        relation = BioCRelation()
        if 'id' in rtree.attrib:
            relation.id = rtree.attrib['id']

        relation.infons = self.__parse_infons(rtree)
        for ntree in rtree.findall('node'):
            relation.add_node(BioCNode(ntree.attrib['refid'], ntree.attrib['role']))

        return relation

    def __parse_infons(self, tree):
        infons = dict()
        for infon_xml in tree.findall('infon'):
            infons[infon_xml.attrib['key']] = infon_xml.text
        return infons
