import lxml.etree as etree

from bioc import BioCCollection, BioCDocument, BioCLocation, BioCNode, BioCRelation, \
    BioCAnnotation, BioCSentence, BioCPassage


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
    doc = etree.ElementTree(BioCXMLEncoder().default(collection))
    s = etree.tostring(doc, pretty_print=pretty_print, encoding=collection.encoding,
                       standalone=collection.standalone)
    return s.decode(collection.encoding)


def encode_location(obj):
    return etree.Element('location', {'offset': str(obj.offset), 'length': str(obj.length)})


def encode_node(obj):
    return etree.Element('node', {'refid': obj.refid, 'role': obj.role})


def encode_relation(obj):
    tree = etree.Element('relation', {'id': obj.id})
    encode_infons(tree, obj.infons)
    for n in obj.nodes:
        tree.append(encode_node(n))
    return tree


def encode_infons(tree, infons):
    for k, v in infons.items():
        elem = encode_infon(k, v)
        tree.append(elem)


def encode_infon(k, v):
    elem = etree.Element('infon', {'key': str(k)})
    elem.text = str(v)
    return elem


def encode_annotation(obj):
    tree = etree.Element('annotation', {'id': obj.id})
    encode_infons(tree, obj.infons)
    for l in obj.locations:
        tree.append(encode_location(l))
    etree.SubElement(tree, 'text').text = obj.text
    return tree


def encode_sentence(obj):
    tree = etree.Element('sentence')
    encode_infons(tree, obj.infons)
    etree.SubElement(tree, 'offset').text = str(obj.offset)
    if obj.text:
        etree.SubElement(tree, 'text').text = obj.text
    for a in obj.annotations:
        tree.append(encode_annotation(a))
    for r in obj.relations:
        tree.append(encode_relation(r))
    return tree


def encode_passage(obj):
    tree = etree.Element('passage')
    encode_infons(tree, obj.infons)
    etree.SubElement(tree, 'offset').text = str(obj.offset)
    if obj.text:
        etree.SubElement(tree, 'text').text = obj.text
    for s in obj.sentences:
        tree.append(encode_sentence(s))
    for a in obj.annotations:
        tree.append(encode_annotation(a))
    for r in obj.relations:
        tree.append(encode_relation(r))
    return tree


def encode_document(obj):
    tree = etree.Element('document')
    etree.SubElement(tree, 'id').text = obj.id
    encode_infons(tree, obj.infons)
    for p in obj.passages:
        tree.append(encode_passage(p))
    for a in obj.annotations:
        tree.append(encode_annotation(a))
    for r in obj.relations:
        tree.append(encode_relation(r))
    return tree


def encode_collection(obj):
    tree = etree.Element('collection')
    etree.SubElement(tree, 'source').text = obj.source
    etree.SubElement(tree, 'date').text = obj.date
    etree.SubElement(tree, 'key').text = obj.key
    encode_infons(tree, obj.infons)
    for d in obj.documents:
        tree.append(encode_document(d))
    return tree


class BioCXMLEncoder(object):
    """
    Extensible BioC XML encoder for BioC data structures.

    To extend this to recognize other objects, subclass and implement a ``.default()`` method
    with another method that returns an XML tree for ``o`` if possible, otherwise it should
    call the superclass implementation.
    """

    def default(self, obj):
        """Implement this method in a subclass such that it returns a tree for ``o``."""
        if isinstance(obj, BioCLocation):
            return encode_location(obj)
        elif isinstance(obj, BioCNode):
            return encode_node(obj)
        elif isinstance(obj, BioCRelation):
            return encode_relation(obj)
        elif isinstance(obj, BioCAnnotation):
            return encode_annotation(obj)
        elif isinstance(obj, BioCSentence):
            return encode_sentence(obj)
        elif isinstance(obj, BioCPassage):
            return encode_passage(obj)
        elif isinstance(obj, BioCDocument):
            return encode_document(obj)
        elif isinstance(obj, BioCCollection):
            return encode_collection(obj)
        else:
            raise TypeError(f'Object of type {obj.__class__.__name__} is not BioC XML serializable')

    def encode(self, o):
        return self.default(o)


class BioCXMLDocumentWriter(object):
    def __init__(self, file, encoding='utf8', standalone=True):
        self.encoding = encoding
        self.standalone = standalone
        self.file = file
        self.encoder = BioCXMLEncoder()
        self.w = self.__writer__()
        next(self.w)  # start writing (run up to 'yield')

    def __writer__(self):
        with etree.xmlfile(self.file, encoding=self.encoding, close=True) as xf:
            xf.write_declaration(standalone=self.standalone)
            with xf.element('collection'):
                try:
                    while True:
                        el = (yield)
                        xf.write(el)
                        xf.write('\n')
                        xf.flush()
                except GeneratorExit:
                    pass

    def write_collection_info(self, collection):
        elem = etree.Element('source')
        elem.text = collection.source
        self.w.send(elem)

        elem = etree.Element('date')
        elem.text = collection.date
        self.w.send(elem)

        elem = etree.Element('key')
        elem.text = collection.key
        self.w.send(elem)

        for k, v in collection.infons.items():
            elem = etree.Element('infon', {'key': str(k)})
            elem.text = str(v)
            self.w.send(elem)

    def close(self):
        self.w.close()

    def write_document(self, document: BioCDocument):
        tree = self.encoder.default(document)
        self.w.send(tree)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
