import lxml.etree as etree


class BioCEncoder(object):
    def __init__(self, pretty_print=True):
        """
        Constructor for BioCEncoder, with sensible defaults.

        Args:
            pretty_print(boolean): enables formatted XML
        """
        self.pretty_print = pretty_print

    def encode(self, collection):
        """
        Return a BioC formatted string representation of a BioC collection structure.

        Args:
            collection(BioCCollection): a BioC collection

        Returns:
            str: a BioC formatted ``str``
        """
        doc = etree.ElementTree(BioCEncoder.to_element_tree(collection))
        return etree.tostring(doc, pretty_print=self.pretty_print, encoding=collection.encoding,
                              standalone=collection.standalone)

    @classmethod
    def to_element_tree(cls, collection):
        """
        Returns the BioC xml tree that the BioCollection represents as a ElementTree.

        Args:
            collection(BioCCollection): a BioC collection

        Returns:
            ElementTree: the BioC xml that the BioCollection represents as a ElementTree.
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
