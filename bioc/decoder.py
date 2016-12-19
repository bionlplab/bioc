import lxml.etree as etree
from io import BytesIO

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
        tree = etree.parse(BytesIO(s))
        collection = self.__parse_collection(tree.getroot())
        collection.encoding = tree.docinfo.encoding
        collection.standalone = tree.docinfo.standalone
        collection.version = tree.docinfo.xml_version
        return collection

    def __parse_collection(self, tree):
        collection = BioCCollection()
        collection.source = tree.findtext('source')
        collection.date = tree.findtext('date')
        collection.key = tree.findtext('key')
        collection.infons = self.__parse_infons(tree)
        for child in tree.findall('document'):
            collection.add_document(self.__parse_document(child))
        return collection

    def __parse_document(self, tree):
        document = BioCDocument()
        document.id = tree.findtext('id')
        document.infons = self.__parse_infons(tree)
        for child in tree.findall('passage'):
            document.add_passage(self.__parse_passage(child))
        for child in tree.findall('annotation'):
            document.add_annotation(self.__parse_annotation(child))
        for child in tree.findall('relation'):
            document.add_relation(self.__parse_relation(child))
        return document

    def __parse_passage(self, tree):
        passage = BioCPassage()
        passage.offset = int(tree.findtext('offset'))
        passage.infons = self.__parse_infons(tree)
        if tree.find('text') is not None:
            passage.text = tree.findtext('text')
        for child in tree.findall('sentence'):
            passage.add_sentence(self.__parse_sentence(child))
        for child in tree.findall('annotation'):
            passage.add_annotation(self.__parse_annotation(child))
        for child in tree.findall('relation'):
            passage.add_relation(self.__parse_relation(child))
        return passage

    def __parse_sentence(self, tree):
        sentence = BioCSentence()
        sentence.offset = int(tree.findtext('offset'))
        sentence.text = tree.findtext('text')
        sentence.infons = self.__parse_infons(tree)
        for child in tree.findall('annotation'):
            sentence.add_annotation(self.__parse_annotation(child))
        for child in tree.findall('relation'):
            sentence.add_relation(self.__parse_relation(child))
        return sentence

    def __parse_annotation(self, tree):
        annotation = BioCAnnotation()
        annotation.id = tree.attrib['id']
        annotation.infons = self.__parse_infons(tree)
        annotation.text = tree.findtext('text')
        for child in tree.findall('location'):
            annotation.add_location(
                BioCLocation(int(child.attrib['offset']), int(child.attrib['length'])))
        return annotation

    def __parse_relation(self, tree):
        relation = BioCRelation()
        if 'id' in tree.attrib:
            relation.id = tree.attrib['id']
        relation.infons = self.__parse_infons(tree)
        for child in tree.findall('node'):
            relation.add_node(BioCNode(child.attrib['refid'], child.attrib['role']))
        return relation

    def __parse_infons(self, tree):
        return {child.attrib['key']: child.text for child in tree.findall('infon')}
