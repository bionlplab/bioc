from contextlib import contextmanager

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
from .decoder import BioCDecoder
from .encoder import BioCEncoder
from .iterdecoder import BioCDecoderIter
from .iterencoder import BioCEncoderIter
from .validator import BioCValidator
from .biocitertools import (
    PASSAGE,
    SENTENCE,
    DOCUMENT,
    annotations,
    relations,
    sentences,
)
from .utils import (
    get_text,
    pretty_print
)

from .jsonencoder import jsondumps

__all__ = ['BioCAnnotation', 'BioCCollection', 'BioCDocument', 'BioCLocation', 'BioCNode',
           'BioCPassage', 'BioCRelation', 'BioCSentence', 'load', 'loads', 'dump', 'dumps',
           'iterparse', 'merge', 'validate', 'iterwrite', 'annotations', 'sentences', 'jsondumps',
           'get_text', 'pretty_print']


def dumps(collection, pretty_print=True):
    """
    Serialize ``collection`` to a BioC formatted ``str``.

    Args:
        collection (BioCollection): the BioC collection
        pretty_print (boolean): enables formatted XML

    Returns:
        str: a BioC formatted ``str``
    """
    return BioCEncoder(pretty_print=pretty_print).encode(collection)


def dump(collection, fp, pretty_print=True):
    """
    Serialize ``collection`` as a BioC formatted stream to ``fp``.

    Args:
        collection (BioCollection): the BioC collection
        fp: a ``.write()``-supporting file-like object
        pretty_print (boolean): enables formatted XML
    """
    fp.write(BioCEncoder(pretty_print=pretty_print).encode(collection))


def load(fp):
    """
    Deserialize ``fp`` to a BioC collection object.

    Args:
        fp: a ``.read()``-supporting file-like object containing a BioC collection

    Returns:
         BioCCollection: a object of BioCollection
    """
    return BioCDecoder().decode(fp)


def loads(s, encoding='UTF-8'):
    """
    Deserialize ``s`` to a BioC collection object.

    Args:
        s(str/bytes/bytearray): a ``str`` instance containing a BioC collection
        encoding(str): The input encoding should be UTF-8, UTF-16 or UTF-32.

    Returns:
        BioCCollection: a object of BioCollection
    """
    return BioCDecoder().decodes(s)


def validate(collection, onerror=None):
    BioCValidator(onerror).validate(collection)


def merge(dst, srcs):
    """
    Merge multiple BioC files into one.

    Args:
        dst(str): output BioC file name
        srcs(list): input BioC file names
    """
    collection = None
    for src in srcs:
        with open(src) as fp:
            tmp = load(fp)
        if collection is None:
            collection = tmp
        else:
            for document in tmp.documents:
                collection.add_document(document)
    with open(dst, 'w') as fp:
        dump(collection, fp)


@contextmanager
def iterparse(file):
    parser = BioCDecoderIter(file)
    yield parser


@contextmanager
def iterwrite(file, collection=None):
    writer = BioCEncoderIter(file, collection)
    yield writer
    writer.close()
