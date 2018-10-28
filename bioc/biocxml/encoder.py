import lxml.etree as etree
from bioc import BioCCollection, BioCDocument


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
    doc = etree.ElementTree(encode_collection(collection))
    s = etree.tostring(doc, pretty_print=pretty_print, encoding=collection.encoding, standalone=collection.standalone)
    return s.decode(collection.encoding)


def to_xml(collection, file):
    with open(file, 'w') as fp:
        dump(collection, fp)


def encode_collection(collection: BioCCollection) -> etree.ElementTree:
    """
    Returns the BioC biocxml tree that the BioCollection represents as a ElementTree.

    Args:
        collection: a BioC collection

    Returns:
        ElementTree: the BioC biocxml that the BioCollection represents as a ElementTree.
    """
    tree = etree.Element('collection')
    etree.SubElement(tree, 'source').text = collection.source
    etree.SubElement(tree, 'date').text = collection.date
    etree.SubElement(tree, 'key').text = collection.key
    for k, v in collection.infons.items():
        tree.append(encode_infon(k, v))
    for d in collection.documents:
        tree.append(encode_document(d))
    return tree


def encode_document(document):
    tree = etree.Element('document')
    etree.SubElement(tree, 'id').text = document.id
    for k, v in document.infons.items():
        tree.append(encode_infon(k, v))
    for p in document.passages:
        tree.append(encode_passage(p))
    for a in document.annotations:
        tree.append(encode_annotation(a))
    for r in document.relations:
        tree.append(encode_relation(r))
    return tree


def encode_passage(passage):
    tree = etree.Element('passage')
    etree.SubElement(tree, 'offset').text = str(passage.offset)
    if passage.text:
        etree.SubElement(tree, 'text').text = passage.text
    for k, v in passage.infons.items():
        tree.append(encode_infon(k, v))
    for s in passage.sentences:
        tree.append(encode_sentence(s))
    for a in passage.annotations:
        tree.append(encode_annotation(a))
    for r in passage.relations:
        tree.append(encode_relation(r))
    return tree


def encode_sentence(sentence):
    tree = etree.Element('sentence')
    for k, v in sentence.infons.items():
        tree.append(encode_infon(k, v))
    etree.SubElement(tree, 'offset').text = str(sentence.offset)
    if sentence.text:
        etree.SubElement(tree, 'text').text = sentence.text
    for a in sentence.annotations:
        tree.append(encode_annotation(a))
    for r in sentence.relations:
        tree.append(encode_relation(r))
    return tree


def encode_annotation(annotation):
    tree = etree.Element('annotation', {'id': annotation.id})
    for k, v in annotation.infons.items():
        tree.append(encode_infon(k, v))
    for l in annotation.locations:
        etree.SubElement(tree, 'location', {'offset': str(l.offset), 'length': str(l.length)})
    etree.SubElement(tree, 'text').text = annotation.text
    return tree


def encode_relation(relation):
    tree = etree.Element('relation', {'id': relation.id})
    for k, v in relation.infons.items():
        tree.append(encode_infon(k, v))
    for n in relation.nodes:
        etree.SubElement(tree, 'node', {'refid': n.refid, 'role': n.role})
    return tree


def encode_infon(k, v):
    elem = etree.Element('infon', {'key': str(k)})
    elem.text = str(v)
    return elem


class BioCXMLDocumentWriter(object):
    def __init__(self, file, encoding='utf8', standalone=True, **kwargs):
        self.encoding = encoding
        self.standalone = standalone
        self.file = file
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
            elem = encode_infon(k, v)
            self.w.send(elem)

    def close(self):
        self.w.close()

    def write_document(self, document: BioCDocument):
        tree = encode_document(document)
        self.w.send(tree)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()