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

from .encoder import BioCEncoder
from .decoder import BioCDecoder
from .validator import BioCValidator
from .iterdecoder import BioCDecoderIter
from .iterencoder import BioCEncoderIter

__all__ = ['BioCAnnotation', 'BioCCollection', 'BioCDocument', 'BioCLocation', 'BioCNode',
           'BioCPassage', 'BioCRelation', 'BioCSentence', 'load', 'loads', 'dump', 'dumps',
           'iterparse', 'merge', 'validate', 'iterwrite']


def dumps(collection, pretty_print=True):
    """
    Serialize ``collection`` to a BioC formatted ``str``.
    :param collection: the BioCollection
    :param pretty_print: (bool) enables formatted XML
    :return: a BioC formatted ``str``
    """
    return BioCEncoder(pretty_print=pretty_print).encode(collection)


def dump(collection, fp, pretty_print=True):
    """
    Serialize ``collection`` as a BioC formatted stream to ``fp``.
    :param collection: the BioCollection
    :param pretty_print: (bool) enables formatted XML
    :param fp: (a ``.write()``-supporting file-like object
    """
    fp.write(BioCEncoder(pretty_print=pretty_print).encode(collection))


def load(fp):
    """
    Deserialize ``fp`` to a BioC collection object.
    :param fp: a ``.read()``-supporting file-like object containing a BioC collection
    :return a object of BioCollection
    """
    return loads(fp.read())


def loads(s):
    """
    Deserialize ``s`` to a BioC collection object.
    :param s: a ``str`` instance containing a BioC collection
    :return a object of BioCollection
    """
    return BioCDecoder().decode(s)


def validate(colllection):
    BioCValidator().validate(colllection)


def merge(dst, srcs):
    """
    Merge multiple BioC files into one.
    :param dst: output BioC file name.
    :type dst: str
    :param srcs: input BioC file names
    :type srcs: list
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
