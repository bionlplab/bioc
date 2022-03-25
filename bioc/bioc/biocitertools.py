"""
This module implements a number of iterator building blocks.
"""

from typing import Generator, Collection, Union

from bioc.bioc import BioCCollection, BioCDocument, BioCPassage, BioCSentence, BioCAnnotation, \
    BioCRelation
from bioc.bioc.constants import DOCUMENT, PASSAGE, SENTENCE


class BioCResult:
    def __init__(self):
        self.document = None  # type: BioCDocument or None
        self.passage = None  # type: BioCPassage or None
        self.sentence = None  # type: BioCSentence or None
        self.annotation = None  # type: BioCAnnotation or None
        self.relation = None  # type: BioCRelation or None


def annotations(obj: BioCCollection or BioCDocument or BioCPassage or BioCSentence,
                docid: str = None,
                level: Union[int, Collection[int]] = (DOCUMENT, PASSAGE, SENTENCE)) \
        -> Generator[BioCResult, None, None]:
    """
    Get all annotations in document id.

    Args:
        obj: BioCCollection, BioCDocument, BioCPassage, or BioCSentence
        docid: document id. If None, all documents
        level: DOCUMENT, PASSAGE, SENTENCE

    Yields:
        one annotation
    """
    if type(level) == int:
        level = (level, )
    if isinstance(obj, BioCCollection):
        for document in filter(lambda d: docid is None or docid == d.id, obj.documents):
            yield from annotations(document, level=level)
    elif isinstance(obj, BioCDocument):
        if DOCUMENT in level:
            for ann in obj.annotations:
                r = BioCResult()
                r.document = obj
                r.annotation = ann
                yield r
        for passage in obj.passages:
            for r in annotations(passage, level=level):
                r.document = obj
                yield r
    elif isinstance(obj, BioCPassage):
        if PASSAGE in level:
            for ann in obj.annotations:
                r = BioCResult()
                r.passage = obj
                r.annotation = ann
                yield r
        for sentence in obj.sentences:
            for r in annotations(sentence, level=level):
                r.passage = obj
                yield r
    elif isinstance(obj, BioCSentence):
        if SENTENCE in level:
            for ann in obj.annotations:
                r = BioCResult()
                r.sentence = obj
                r.annotation = ann
                yield r
    else:
        raise TypeError(f'Object of type {obj.__class__.__name__} must be BioCCollection, '
                        f'BioCDocument, BioCPassage, or BioCSentence')


def relations(obj: BioCCollection or BioCDocument or BioCPassage or BioCSentence,
              docid: str = None,
              level: Union[int, Collection[int]] = (DOCUMENT, PASSAGE, SENTENCE)) \
        -> Generator[BioCResult, None, None]:
    """
    Get all relations in document id.

    Args:
        obj: BioCCollection, BioCDocument, BioCPassage, or BioCSentence
        docid: document id. If None, all documents
        level: DOCUMENT, PASSAGE, SENTENCE

    Yields:
        one relation
    """
    if type(level) == int:
        level = (level, )
    if isinstance(obj, BioCCollection):
        for document in filter(lambda d: docid is None or docid == d.id, obj.documents):
            yield from relations(document, level=level)
    elif isinstance(obj, BioCDocument):
        if DOCUMENT in level:
            for rel in obj.relations:
                r = BioCResult()
                r.document = obj
                r.relation = rel
                yield r
        for passage in obj.passages:
            for r in relations(passage, level=level):
                r.document = obj
                yield r
    elif isinstance(obj, BioCPassage):
        if PASSAGE in level:
            for rel in obj.relations:
                r = BioCResult()
                r.passage = obj
                r.relation = rel
                yield r
        for sentence in obj.sentences:
            for r in relations(sentence, level=level):
                r.passage = obj
                yield r
    elif isinstance(obj, BioCSentence):
        if SENTENCE in level:
            for rel in obj.relations:
                r = BioCResult()
                r.sentence = obj
                r.relation = rel
                yield r
    else:
        raise TypeError(f'Object of type {obj.__class__.__name__} must be BioCCollection, '
                        f'BioCDocument, BioCPassage, or BioCSentence')


def sentences(obj: BioCCollection or BioCDocument or BioCPassage) -> Generator[BioCResult, None, None]:
    """
    Get all sentences in document id.

    Args:
        obj: BioCCollection, BioCDocument, or BioCPassage

    Yields:
        one sentence
    """
    if isinstance(obj, BioCCollection):
        for document in obj.documents:
            yield from sentences(document)
    elif isinstance(obj, BioCDocument):
        for passage in obj.passages:
            for r in sentences(passage):
                r.document = obj
                yield r
    elif isinstance(obj, BioCPassage):
        for sentence in obj.sentences:
            r = BioCResult()
            r.passage = obj
            r.sentence = sentence
            yield r
    else:
        raise TypeError(f'Object of type {obj.__class__.__name__} must be BioCCollection, BioCDocument, BioCPassage')
