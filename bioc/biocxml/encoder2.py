"""
BioC XML encoder v2
"""
from typing import TextIO
from lxml import etree

from bioc import BioCCollection, BioCDocument
from bioc.biocxml.encoder import encode_infons, encode_annotation, encode_relation


def dump(collection: BioCCollection, fp: TextIO, *, pretty_print: bool = True):
    """
    Serialize ``collection`` as a BioC formatted stream to ``fp``.

    Args:
        collection: the BioC collection
        fp: a ``.write()``-supporting file-like object
        pretty_print: enables formatted XML
    """
    fp.write(dumps(collection, pretty_print=pretty_print))


def dumps(collection: BioCCollection, *, pretty_print: bool = True) -> str:
    """
    Serialize ``collection`` to a BioC formatted ``str``.

    Args:
        collection: the BioC collection
        pretty_print: enables formatted XML

    Returns:
        a BioC formatted ``str``
    """
    doc = etree.ElementTree(encode_collection(collection))
    s = etree.tostring(doc, pretty_print=pretty_print, encoding=collection.encoding,
                       standalone=collection.standalone)
    return s.decode(collection.encoding)


def encode_sentence(sentence):
    """Encode a single sentence."""
    tree = etree.Element('sentence', {'offset': str(sentence.offset)})
    encode_infons(tree, sentence.infons)
    if sentence.text:
        etree.SubElement(tree, 'text').text = sentence.text
    for ann in sentence.annotations:
        tree.append(encode_annotation(ann))
    for rel in sentence.relations:
        tree.append(encode_relation(rel))
    return tree


def encode_passage(passage):
    """Encode a single passage."""
    tree = etree.Element('passage', {'offset': str(passage.offset)})
    encode_infons(tree, passage.infons)
    if passage.text:
        etree.SubElement(tree, 'text').text = passage.text
    for sen in passage.sentences:
        tree.append(encode_sentence(sen))
    for ann in passage.annotations:
        tree.append(encode_annotation(ann))
    for rel in passage.relations:
        tree.append(encode_relation(rel))
    return tree


def encode_document(document):
    """Encode a single document."""
    tree = etree.Element('document', {'id': str(document.id)})
    encode_infons(tree, document.infons)
    if document.text:
        etree.SubElement(tree, 'text').text = document.text
    for passage in document.passages:
        tree.append(encode_passage(passage))
    for sen in document.sentences:
        tree.append(encode_sentence(sen))
    for ann in document.annotations:
        tree.append(encode_annotation(ann))
    for rel in document.relations:
        tree.append(encode_relation(rel))
    return tree


def encode_collection(collection):
    """Encode a single collection."""
    tree = etree.Element('collection')
    etree.SubElement(tree, 'source').text = collection.source
    etree.SubElement(tree, 'date').text = collection.date
    etree.SubElement(tree, 'key').text = collection.key
    etree.SubElement(tree, 'version').text = collection.version
    encode_infons(tree, collection.infons)
    for doc in collection.documents:
        tree.append(encode_document(doc))
    for sen in collection.sentences:
        tree.append(encode_sentence(sen))
    return tree


class BioCXMLDocumentWriter:
    """
    Writer for the BioC XML format, one document at a time.
    """

    def __init__(self, file, encoding='utf8', standalone=True):
        self.encoding = encoding
        self.standalone = standalone
        self.file = file
        self.__writer = self.__writer__()
        next(self.__writer)  # start writing (run up to 'yield')

    def __writer__(self):
        with etree.xmlfile(self.file, encoding=self.encoding) as xf:
            xf.write_declaration(standalone=self.standalone)
            with xf.element('collection'):
                try:
                    while True:
                        elem = (yield)
                        xf.write(elem)
                        xf.write('\n')
                        xf.flush()
                except GeneratorExit:
                    pass

    def write_collection_info(self, collection: BioCCollection):
        """
        Writes the collection information: encoding, version, DTD, source, date, key, infons, etc.
        """
        elem = etree.Element('source')
        elem.text = collection.source
        self.__writer.send(elem)

        elem = etree.Element('date')
        elem.text = collection.date
        self.__writer.send(elem)

        elem = etree.Element('key')
        elem.text = collection.key
        self.__writer.send(elem)

        elem = etree.Element('version')
        elem.text = collection.version
        self.__writer.send(elem)

        for k, v in collection.infons.items():
            elem = etree.Element('infon', {'key': str(k)})
            elem.text = str(v)
            self.__writer.send(elem)

    def close(self):
        """Close this writer"""
        self.__writer.close()

    def write_document(self, document: BioCDocument):
        """Encode and write a single document."""
        tree = encode_document(document)
        self.__writer.send(tree)

    # def __enter__(self):
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.close()
