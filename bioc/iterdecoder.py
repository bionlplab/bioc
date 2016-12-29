import lxml.etree as etree

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


class BioCDecoderIter:
    """
    Code to read/write BioC XML in an incremental way.
    """

    def __init__(self, name):
        """
        Open an object of the BioCDecoderIter which can parse an BioC file incrementally at document level.
        :param name: file name to be decoded
        """
        self.file = name
        self.__context = iter(etree.iterparse(self.file, events=('start', 'end')))
        self.__state = 0
        self.__read()

    def __iter__(self):
        return self

    def __next__(self):
        if self.__document is None:
            raise StopIteration
        else:
            document = self.__document
            self.__read()
            return document

    def next(self):
        """
        Reads one BioC document from the XML file.

        :return: the BioC document
        :rtype: BioCDocument
        """
        return self.__next__()

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
                    elif elem.tag == 'data':
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
        raise RuntimeError("should not reach here")

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
        raise RuntimeError("should not reach here")

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

        :return: the BioC collection that contains only information
        :rtype: BioCCollection
        """
        return self.__collection
