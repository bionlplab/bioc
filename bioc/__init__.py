from typing import List, TextIO, Callable

from bioc.bioc import BioCCollection, BioCDocument, BioCPassage, BioCSentence, BioCAnnotation, BioCRelation, \
    BioCLocation, BioCNode
from bioc.biocitertools import PASSAGE, SENTENCE, DOCUMENT, annotations, relations, sentences
from bioc.decoder import BioCDecoder
from bioc.encoder import BioCEncoder
from bioc.iterdecoder import BioCDecoderIter
from bioc.iterencoder import BioCEncoderIter
from bioc.utils import get_text, pretty_print
from bioc.validator import BioCValidator

__all__ = ['BioCAnnotation', 'BioCCollection', 'BioCDocument', 'BioCLocation', 'BioCNode',
           'BioCPassage', 'BioCRelation', 'BioCSentence', 'load', 'loads', 'dump', 'dumps',
           'iterparse', 'merge', 'validate', 'iterwrite', 'annotations', 'sentences', 'get_text', 'pretty_print']


def dumps(collection: BioCCollection, pretty_print: bool = True) -> str:
    """
    Serialize ``collection`` to a BioC formatted ``str``.

    Args:
        collection: the BioC collection
        pretty_print: enables formatted XML

    Returns:
        a BioC formatted ``str``
    """
    return BioCEncoder(pretty_print=pretty_print).encode(collection)


def dump(collection: BioCCollection, fp: TextIO, pretty_print: bool = True):
    """
    Serialize ``collection`` as a BioC formatted stream to ``fp``.

    Args:
        collection: the BioC collection
        fp: a ``.write()``-supporting file-like object
        pretty_print: enables formatted XML
    """
    fp.write(BioCEncoder(pretty_print=pretty_print).encode(collection))


def load(fp: TextIO) -> BioCCollection:
    """
    Deserialize ``fp`` to a BioC collection object.

    Args:
        fp: a ``.read()``-supporting file-like object containing a BioC collection

    Returns:
         a object of BioCollection
    """
    return BioCDecoder().decode(fp)


def loads(s: str) -> BioCCollection:
    """
    Deserialize ``s`` to a BioC collection object.

    Args:
        s: a ``str`` instance containing a BioC collection

    Returns:
        an object of BioCollection
    """
    return BioCDecoder().decodes(s)


def validate(collection, onerror: Callable[[str, List], None] = None):
    BioCValidator(onerror).validate(collection)


def merge(output: str, *input: str):
    """
    Merge multiple BioC files into one.

    Args:
        output: output BioC file name
        input: input BioC file names
    """
    collection = None
    for src in input:
        with open(src) as fp:
            tmp = load(fp)
        if collection is None:
            collection = tmp
        else:
            for document in tmp.documents:
                collection.add_document(document)
    with open(output, 'w') as fp:
        dump(collection, fp)


def iterparse(file) -> BioCDecoderIter:
    if not isinstance(file, str):
        file = str(file)
    parser = BioCDecoderIter(file)
    return parser


def iterwrite(file, collection=None) -> BioCEncoderIter:
    if not isinstance(file, str):
        file = str(file)
    writer = BioCEncoderIter(file, collection)
    return writer
