"""
BioC JSON decoder
"""
import io
import json
from contextlib import contextmanager
from typing import TextIO, Dict, Union

from bioc.datastructure import BioCCollection, BioCSentence, \
    BioCRelation, BioCAnnotation, BioCNode, \
    BioCLocation, BioCPassage, BioCDocument


def parse_collection(obj: Dict) -> BioCCollection:
    """
    Deserialize a dict ``obj`` to a BioCCollection object
    """
    collection = BioCCollection()
    collection.source = obj['source']
    collection.date = obj['date']
    collection.key = obj['key']
    if 'version' in obj:
        collection.version = obj['version']
    collection.infons = obj['infons']
    for doc in obj['documents']:
        collection.add_document(parse_doc(doc))
    return collection


def parse_annotation(obj: Dict) -> BioCAnnotation:
    """
    Deserialize a dict obj to a BioCAnnotation object
    """
    ann = BioCAnnotation()
    ann.id = obj['id']
    ann.infons = obj['infons']
    ann.text = obj['text']
    for loc in obj['locations']:
        ann.add_location(BioCLocation(loc['offset'], loc['length']))
    return ann


def parse_relation(obj: Dict) -> BioCRelation:
    """
    Deserialize a dict obj to a BioCRelation object
    """
    rel = BioCRelation()
    rel.id = obj['id']
    rel.infons = obj['infons']
    for node in obj['nodes']:
        rel.add_node(BioCNode(node['refid'], node['role']))
    return rel


def parse_sentence(obj: Dict) -> BioCSentence:
    """
    Deserialize a dict obj to a BioCSentence object
    """
    sentence = BioCSentence()
    sentence.offset = obj['offset']
    sentence.infons = obj['infons']
    sentence.text = obj['text']
    for annotation in obj['annotations']:
        sentence.add_annotation(parse_annotation(annotation))
    for relation in obj['relations']:
        sentence.add_relation(parse_relation(relation))
    return sentence


def parse_passage(obj: Dict) -> BioCPassage:
    """
    Deserialize a dict obj to a BioCPassage object
    """
    passage = BioCPassage()
    passage.offset = obj['offset']
    passage.infons = obj['infons']
    if 'text' in obj:
        passage.text = obj['text']
    for sentence in obj['sentences']:
        passage.add_sentence(parse_sentence(sentence))
    for annotation in obj['annotations']:
        passage.add_annotation(parse_annotation(annotation))
    for relation in obj['relations']:
        passage.add_relation(parse_relation(relation))
    return passage


def parse_doc(obj: Dict) -> BioCDocument:
    """
    Deserialize a dict obj to a BioCDocument object
    """
    doc = BioCDocument()
    doc.id = obj['id']
    doc.infons = obj['infons']
    for passage in obj['passages']:
        doc.add_passage(parse_passage(passage))
    if 'annotations' in obj:
        for annotation in obj['annotations']:
            doc.add_annotation(parse_annotation(annotation))
    for relation in obj['relations']:
        doc.add_relation(parse_relation(relation))
    return doc


def load(fp: TextIO, **kwargs) -> BioCCollection:
    """
    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a JSON document) to a BioCCollection object. kwargs are passed to json.
    """
    obj = json.load(fp, **kwargs)
    return parse_collection(obj)


def loads(s: str, **kwargs) -> BioCCollection:
    """
    Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a JSON document) to a BioCCollection object. kwargs are
    passed to json.
    """
    obj = json.loads(s, **kwargs)
    return parse_collection(obj)


def fromJSON(obj: Dict, bioctype: str = None) \
        -> Union[BioCDocument, BioCPassage, BioCSentence]:
    """
    Convert a Python dict to a BioC object
    """
    if 'bioctype' in obj and bioctype is None:
        bioctype = obj['bioctype']
    if bioctype is None:
        raise KeyError('Cannot find bioctype in the object: %s' % obj)

    if bioctype == 'BioCDocument':
        return parse_doc(obj)
    elif bioctype == 'BioCPassage':
        return parse_passage(obj)
    elif bioctype == 'BioCSentence':
        return parse_sentence(obj)
    else:
        raise KeyError


class BioCJsonIterReader:
    """
    Reader for the jsonlines format.
    """

    def __init__(self, fp: TextIO):
        self.fp = fp
        self.lineno = 0

    def __iter__(self):
        return self

    def __next__(self):
        s = self.fp.readline()
        self.lineno += 1
        if s:
            obj = json.loads(s)
            if 'bioctype' not in obj:
                raise KeyError('%s:%s: Cannot find bioctype in the object: %s'
                               % (self.fp.name, self.lineno, s))
            return fromJSON(obj)
        else:
            raise StopIteration


@contextmanager
def iterreader(source: Union[str, TextIO]) -> BioCJsonIterReader:
    """
    Parse a jsonline into a BioC object incrementally.

    :param file: a filename or file object
    :return: an iterator
    """
    if isinstance(source, io.TextIOBase):
        reader = BioCJsonIterReader(source)
        yield reader
    else:
        with open(source) as fp:
            reader = BioCJsonIterReader(fp)
            yield reader
