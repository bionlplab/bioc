from contextlib import contextmanager
from typing import Generator, List, TextIO, Callable

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

from .jsonencoder import dumps as jsondumps
from .jsonencoder import dump as jsondump
from .jsondecoder import load as jsonload
from .jsondecoder import loads as jsonloads


__all__ = ['BioCAnnotation', 'BioCCollection', 'BioCDocument', 'BioCLocation', 'BioCNode',
           'BioCPassage', 'BioCRelation', 'BioCSentence', 'load', 'loads', 'dump', 'dumps',
           'iterparse', 'merge', 'validate', 'iterwrite', 'annotations', 'sentences', 'jsondumps', 'jsondump',
           'jsonload', 'jsonloads', 'get_text', 'pretty_print']


def dumps(collection: BioCCollection, pretty_print: bool=True) -> str:
    """
    Serialize ``collection`` to a BioC formatted ``str``.

    Args:
        collection: the BioC collection
        pretty_print: enables formatted XML

    Returns:
        a BioC formatted ``str``
    """
    return BioCEncoder(pretty_print=pretty_print).encode(collection)


def dump(collection: BioCCollection, fp: TextIO, pretty_print: bool=True):
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
        s(str/bytes/bytearray): a ``str`` instance containing a BioC collection
        encoding(str): The input encoding should be UTF-8, UTF-16 or UTF-32.

    Returns:
        an object of BioCollection
    """
    return BioCDecoder().decodes(s)


def validate(collection, onerror: Callable[[str, List], None]=None):
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


@contextmanager
def iterparse(file: str) -> Generator[BioCDecoderIter, None, None]:
    parser = BioCDecoderIter(file)
    yield parser


@contextmanager
def iterwrite(file: str, collection=None) -> Generator[BioCEncoderIter, None, None]:
    writer = BioCEncoderIter(file, collection)
    yield writer
    writer.close()
