"""
BioC XML encoder
"""

from lxml import etree

from bioc import BioCCollection, BioCDocument, BioCLocation, BioCNode, BioCRelation


def dump(collection: BioCCollection, fp, pretty_print: bool = True):
    """
    Serialize ``collection`` as a BioC formatted stream to ``fp``.

    Args:
        collection: the BioC collection
        fp: a ``.write()``-supporting file-like object
        pretty_print: enables formatted XML
    """
    fp.write(dumps(collection, pretty_print))


def dumps(collection: BioCCollection, pretty_print: bool = True) -> str:
    """
    Serialize ``collection`` to a BioC formatted ``str``.

    Args:
        collection: the BioC collection
        pretty_print: enables formatted XML

    Returns:
        a BioC formatted ``str``
    """
    doc = etree.ElementTree(BioCXMLEncoder().encode(collection))
    s = etree.tostring(doc, pretty_print=pretty_print, encoding=collection.encoding,
                       standalone=collection.standalone)
    return s.decode(collection.encoding)


def encode_location(location: BioCLocation):
    """Encode a single location."""
    return etree.Element('location',
                         {'offset': str(location.offset), 'length': str(location.length)})


def encode_node(node: BioCNode):
    """Encode a single node."""
    return etree.Element('node', {'refid': node.refid, 'role': node.role})


def encode_relation(relation: BioCRelation):
    """Encode a single relation."""
    tree = etree.Element('relation', {'id': relation.id})
    encode_infons(tree, relation.infons)
    for node in relation.nodes:
        tree.append(encode_node(node))
    return tree


def encode_infons(tree, infons):
    for k, v in infons.items():
        elem = encode_infon(k, v)
        tree.append(elem)


def encode_infon(k, v):
    elem = etree.Element('infon', {'key': str(k)})
    elem.text = str(v)
    return elem


def encode_annotation(annotation):
    """Encode a single annotation."""
    tree = etree.Element('annotation', {'id': annotation.id})
    encode_infons(tree, annotation.infons)
    for location in annotation.locations:
        tree.append(encode_location(location))
    etree.SubElement(tree, 'text').text = annotation.text
    return tree


def encode_sentence(sentence):
    """Encode a single sentence."""
    tree = etree.Element('sentence')
    encode_infons(tree, sentence.infons)
    etree.SubElement(tree, 'offset').text = str(sentence.offset)
    if sentence.text:
        etree.SubElement(tree, 'text').text = sentence.text
    for ann in sentence.annotations:
        tree.append(encode_annotation(ann))
    for rel in sentence.relations:
        tree.append(encode_relation(rel))
    return tree


def encode_passage(passage):
    """Encode a single passage."""
    tree = etree.Element('passage')
    encode_infons(tree, passage.infons)
    etree.SubElement(tree, 'offset').text = str(passage.offset)
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
    tree = etree.Element('document')
    etree.SubElement(tree, 'id').text = document.id
    encode_infons(tree, document.infons)
    for passage in document.passages:
        tree.append(encode_passage(passage))
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
    encode_infons(tree, collection.infons)
    for doc in collection.documents:
        tree.append(encode_document(doc))
    return tree


class BioCXMLEncoder:
    """
    Extensible BioC XML encoder for BioC data structures.

    To extend this to recognize other objects, subclass and implement a ``.default()`` method
    with another method that returns an XML tree for ``o`` if possible, otherwise it should
    call the superclass implementation.
    """

    def default(self, obj):
        """Implement this method in a subclass such that it returns a tree for ``o``."""
        if isinstance(obj, BioCDocument):
            return encode_document(obj)
        if isinstance(obj, BioCCollection):
            return encode_collection(obj)
        raise TypeError(f'Object of type {obj.__class__.__name__} is not BioC XML serializable')

    def encode(self, obj):
        """Encode an obj to an element tree"""
        return self.default(obj)


class BioCXMLDocumentWriter:
    """
    Writer for the BioC XML format, one document at a time.
    """

    def __init__(self, file, encoding='utf8', standalone=True):
        self.encoding = encoding
        self.standalone = standalone
        self.file = file
        self.encoder = BioCXMLEncoder()
        self.__writer = self.__writer__()
        next(self.__writer)  # start writing (run up to 'yield')

    def __writer__(self):
        with etree.xmlfile(self.file, encoding=self.encoding, close=True) as xf:
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

        for k, v in collection.infons.items():
            elem = etree.Element('infon', {'key': str(k)})
            elem.text = str(v)
            self.__writer.send(elem)

    def close(self):
        """Close this writer"""
        self.__writer.close()

    def write_document(self, document: BioCDocument):
        """Encode and write a single document."""
        tree = self.encoder.encode(document)
        self.__writer.send(tree)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
