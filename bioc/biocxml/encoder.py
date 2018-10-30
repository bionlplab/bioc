import lxml.etree as etree
from bioc import BioCCollection, BioCDocument, BioCLocation, BioCNode, BioCRelation, BioCAnnotation, BioCSentence, \
    BioCPassage


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
    s = etree.tostring(doc, pretty_print=pretty_print, encoding=collection.encoding, standalone=collection.standalone)
    return s.decode(collection.encoding)


class BioCXMLEncoder():
    def default(self, obj):
        if isinstance(obj, BioCLocation):
            return etree.Element('location', {'offset': str(obj.offset), 'length': str(obj.length)})
        elif isinstance(obj, BioCNode):
            return etree.Element('node', {'refid': obj.refid, 'role': obj.role})
        elif isinstance(obj, BioCRelation):
            tree = etree.Element('relation', {'id': obj.id})
            self.encode_infon(tree, obj.infons)
            for n in obj.nodes:
                tree.append(self.default(n))
            return tree
        elif isinstance(obj, BioCAnnotation):
            tree = etree.Element('annotation', {'id': obj.id})
            self.encode_infon(tree, obj.infons)
            for l in obj.locations:
                tree.append(self.default(l))
            etree.SubElement(tree, 'text').text = obj.text
            return tree
        elif isinstance(obj, BioCSentence):
            tree = etree.Element('sentence')
            self.encode_infon(tree, obj.infons)
            etree.SubElement(tree, 'offset').text = str(obj.offset)
            if obj.text:
                etree.SubElement(tree, 'text').text = obj.text
            for a in obj.annotations:
                tree.append(self.default(a))
            for r in obj.relations:
                tree.append(self.default(r))
            return tree
        elif isinstance(obj, BioCPassage):
            tree = etree.Element('passage')
            self.encode_infon(tree, obj.infons)
            etree.SubElement(tree, 'offset').text = str(obj.offset)
            if obj.text:
                etree.SubElement(tree, 'text').text = obj.text
            for s in obj.sentences:
                tree.append(self.default(s))
            for a in obj.annotations:
                tree.append(self.default(a))
            for r in obj.relations:
                tree.append(self.default(r))
            return tree
        elif isinstance(obj, BioCDocument):
            tree = etree.Element('document')
            etree.SubElement(tree, 'id').text = obj.id
            self.encode_infon(tree, obj.infons)
            for p in obj.passages:
                tree.append(self.default(p))
            for a in obj.annotations:
                tree.append(self.default(a))
            for r in obj.relations:
                tree.append(self.default(r))
            return tree
        elif isinstance(obj, BioCCollection):
            tree = etree.Element('collection')
            etree.SubElement(tree, 'source').text = obj.source
            etree.SubElement(tree, 'date').text = obj.date
            etree.SubElement(tree, 'key').text = obj.key
            self.encode_infon(tree, obj.infons)
            for d in obj.documents:
                tree.append(self.default(d))
            return tree
        else:
            raise ValueError

    @staticmethod
    def encode_infon(tree, infons):
        for k, v in infons.items():
            elem = etree.Element('infon', {'key': str(k)})
            elem.text = str(v)
            tree.append(elem)


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
