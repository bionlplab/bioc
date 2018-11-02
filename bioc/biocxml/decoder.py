"""
BioC XML decoder
"""

import io
from typing import TextIO

from lxml import etree

from bioc import BioCCollection, BioCDocument, BioCPassage, BioCSentence, BioCAnnotation, \
    BioCRelation, BioCLocation, BioCNode


class BioCXMLDecoder:
    """
    Reader for the BioC XML format.
    """

    def __init__(self):
        pass

    def decodes(self, s: str) -> BioCCollection:
        """
        Deserialize ``s`` to a BioC collection object.

        Args:
            s: a "str" instance containing a BioC collection

        Returns:
            an object of BioCollection
        """
        tree = etree.parse(io.BytesIO(bytes(s, encoding='UTF-8')))
        collection = self.__parse_collection(tree.getroot())
        collection.encoding = tree.docinfo.encoding
        collection.standalone = tree.docinfo.standalone
        collection.version = tree.docinfo.xml_version
        return collection

    def decode(self, fp: TextIO) -> BioCCollection:
        """
        Deserialize ``fp`` to a BioC collection object.

        Args:
            fp: a ``.read()``-supporting file-like object containing a BioC collection

        Returns:
            an object of BioCollection
        """
        # utf8_parser = etree.XMLParser(encoding='utf-8')
        tree = etree.parse(fp)
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

    @classmethod
    def __parse_infons(cls, tree):
        return {child.attrib['key']: child.text for child in tree.findall('infon')}


class BioCXMLDocumentReader:
    """
    Reader for the BioC XML format, one document per iteration.
    """

    def __init__(self, file):
        if not isinstance(file, str):
            file = str(file)
        self.file = file
        self.__context = iter(etree.iterparse(self.file, events=('start', 'end')))
        self.__state = 0
        self.__event = None
        self.__elem = None
        self.__read()

    def __iter__(self):
        return self

    def __next__(self):
        """
        Reads one BioC document from the XML file.

        Returns:
            BioCDocument: the BioC document
        """
        if self.__document is None:
            raise StopIteration
        else:
            document = self.__document
            self.__read()
            return document

    def __read(self):
        while self.__has_next():
            event, elem = self.__next_event()
            if self.__state == 0:
                if event == 'start':
                    if elem.tag == 'collection':
                        self.__state = 1
                        self.__collection = BioCCollection()
                        # collection information
            elif self.__state == 1:
                if event == 'start':
                    if elem.tag == 'document':
                        self.__document = BioCDocument()
                        self.__state = 2
                elif event == 'end':
                    if elem.tag == 'source':
                        self.__collection.source = elem.text
                    elif elem.tag == 'date':
                        self.__collection.date = elem.text
                    elif elem.tag == 'key':
                        self.__collection.key = elem.text
                    elif elem.tag == 'infon':
                        self.__collection.infons[elem.get('key')] = elem.text
                    elif elem.tag == 'collection':
                        self.__state = 0
                        self.__document = None
                        self.__passage = None
                        self.__sentence = None
            elif self.__state == 2:
                if event == 'start':
                    if elem.tag == 'passage':
                        self.__passage = BioCPassage()
                        self.__state = 3
                    elif elem.tag == 'annotation':
                        self.__document.add_annotation(self.__read_annotation(elem))
                    elif elem.tag == 'relation':
                        self.__document.add_relation(self.__read_relation(elem))
                elif event == 'end':
                    if elem.tag == 'id':
                        self.__document.id = elem.text
                    elif elem.tag == 'infon':
                        self.__document.infons[elem.get('key')] = elem.text
                    elif elem.tag == 'document':
                        self.__state = 1
                        return
            elif self.__state == 3:
                if event == 'start':
                    if elem.tag == 'sentence':
                        self.__sentence = BioCSentence()
                        self.__state = 4
                    elif elem.tag == 'annotation':
                        self.__passage.add_annotation(self.__read_annotation(elem))
                    elif elem.tag == 'relation':
                        self.__passage.add_relation(self.__read_relation(elem))
                elif event == 'end':
                    if elem.tag == 'offset':
                        self.__passage.offset = int(elem.text)
                    elif elem.tag == 'text':
                        self.__passage.text = elem.text
                    elif elem.tag == 'infon':
                        self.__passage.infons[elem.get('key')] = elem.text
                    elif elem.tag == 'passage':
                        self.__state = 2
                        if self.__passage is not None:
                            self.__document.add_passage(self.__passage)
            elif self.__state == 4:
                if event == 'start':
                    if elem.tag == 'annotation':
                        self.__sentence.add_annotation(self.__read_annotation(elem))
                    elif elem.tag == 'relation':
                        self.__sentence.add_relation(self.__read_relation(elem))
                elif event == 'end':
                    if elem.tag == 'offset':
                        self.__sentence.offset = int(elem.text)
                    elif elem.tag == 'text':
                        self.__sentence.text = elem.text
                    elif elem.tag == 'infon':
                        self.__sentence.infons[elem.get('key')] = elem.text
                    elif elem.tag == 'sentence':
                        self.__state = 3
                        if self.__sentence is not None:
                            self.__passage.add_sentence(self.__sentence)

    def __read_annotation(self, start_elem):
        ann = BioCAnnotation()
        ann.id = start_elem.get('id')
        while self.__has_next():
            event, elem = self.__next_event()
            if event == 'start':
                pass
            elif event == 'end':
                if elem.tag == 'text':
                    ann.text = elem.text
                elif elem.tag == 'infon':
                    ann.infons[elem.get('key')] = elem.text
                elif elem.tag == 'location':
                    ann.add_location(BioCLocation(int(elem.get('offset')), int(elem.get('length'))))
                elif elem.tag == 'annotation':
                    return ann
        raise RuntimeError("should not reach here")  # pragma: no cover

    def __read_relation(self, start_elem):
        rel = BioCRelation()
        rel.id = start_elem.get('id')
        while self.__has_next():
            event, elem = self.__next_event()
            if event == 'start':
                pass
            elif event == 'end':
                if elem.tag == 'infon':
                    rel.infons[elem.get('key')] = elem.text
                elif elem.tag == 'node':
                    rel.add_node(BioCNode(elem.get('refid'), elem.get('role')))
                if elem.tag == 'relation':
                    return rel
        raise RuntimeError("should not reach here")  # pragma: no cover

    def __has_next(self):
        try:
            self.__event, self.__elem = next(self.__context)
            return True
        except StopIteration:
            self.__event = None
            self.__elem = None
            return False

    def __next_event(self):
        return self.__event, self.__elem

    def get_collection_info(self):
        """
        Reads the collection information: encoding, version, DTD, source, date, key, infons, etc.

        Returns:
            BioCCollection: the BioC collection that contains only information
        """
        return self.__collection

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close this reader"""
        pass


def load(fp) -> BioCCollection:
    """
    Deserialize ``fp`` to a BioC collection object.

    Args:
        fp: a ``.read()``-supporting file-like object containing a BioC collection

    Returns:
         a object of BioCollection
    """
    return BioCXMLDecoder().decode(fp)


def loads(s: str) -> BioCCollection:
    """
    Deserialize ``s`` to a BioC collection object.

    Args:
        s: a ``str`` instance containing a BioC collection

    Returns:
        an object of BioCollection
    """
    return BioCXMLDecoder().decodes(s)
