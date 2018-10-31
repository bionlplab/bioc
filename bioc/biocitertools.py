"""
This module implements a number of iterator building blocks.
"""

from typing import Generator

from bioc import BioCCollection, BioCDocument, BioCPassage, BioCSentence, BioCAnnotation, \
    BioCRelation
from bioc.constants import PASSAGE, DOCUMENT, SENTENCE


def annotations(obj: BioCCollection or BioCDocument or BioCPassage or BioCSentence,
                docid: str = None, level: int = PASSAGE) -> Generator[BioCAnnotation, None, None]:
    """
    Get all annotations in document id.

    Args:
        obj: BioCCollection, BioCDocument, BioCPassage, or BioCSentence
        docid: document id. If None, all documents
        level: one of DOCUMENT, PASSAGE, SENTENCE

    Yields:
        one annotation
    """
    if isinstance(obj, BioCCollection):
        for document in filter(lambda d: docid is None or docid == d.id, obj.documents):
            yield from annotations(document, level=level)
    elif isinstance(obj, BioCDocument):
        if level == DOCUMENT:
            yield from obj.annotations
        elif level in (PASSAGE, SENTENCE):
            for passage in obj.passages:
                yield from annotations(passage, level=level)
        else:
            raise ValueError('level must be DOCUMENT, PASSAGE, or SENTENCE')
    elif isinstance(obj, BioCPassage):
        if level == PASSAGE:
            yield from obj.annotations
        elif level == SENTENCE:
            for sentence in obj.sentences:
                yield from annotations(sentence, level=level)
        else:
            raise ValueError('level must be PASSAGE or SENTENCE')
    elif isinstance(obj, BioCSentence):
        if level == SENTENCE:
            yield from obj.annotations
        else:
            raise ValueError('level must be SENTENCE')
    else:
        raise TypeError(f'Object of type {obj.__class__.__name__} must be BioCCollection, '
                        f'BioCDocument, BioCPassage, or BioCSentence')


def relations(obj: BioCCollection or BioCDocument or BioCPassage or BioCSentence,
              docid: str = None, level: int = PASSAGE) -> Generator[BioCRelation, None, None]:
    """
    Get all relations in document id.

    Args:
        obj: BioCCollection, BioCDocument, BioCPassage, or BioCSentence
        docid: document id. If None, all documents
        level: one of DOCUMENT, PASSAGE, SENTENCE

    Yields:
        one relation
    """
    if isinstance(obj, BioCCollection):
        for document in filter(lambda d: docid is None or docid == d.id, obj.documents):
            yield from relations(document, level=level)
    elif isinstance(obj, BioCDocument):
        if level == DOCUMENT:
            yield from obj.relations
        elif level in (PASSAGE, SENTENCE):
            for passage in obj.passages:
                yield from relations(passage, level=level)
        else:
            raise ValueError('level must be DOCUMENT, PASSAGE, or SENTENCE')
    elif isinstance(obj, BioCPassage):
        if level == PASSAGE:
            yield from obj.relations
        elif level == SENTENCE:
            for sentence in obj.sentences:
                yield from relations(sentence, level=level)
        else:
            raise ValueError('level must be PASSAGE or SENTENCE')
    elif isinstance(obj, BioCSentence):
        if level == SENTENCE:
            yield from obj.relations
        else:
            raise ValueError('level must be SENTENCE')
    else:
        raise TypeError(f'Object of type {obj.__class__.__name__} must be BioCCollection, '
                        f'BioCDocument, BioCPassage, or BioCSentence')


def sentences(obj: BioCCollection or BioCDocument or BioCPassage) \
        -> Generator[BioCSentence, None, None]:
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
            yield from sentences(passage)
    elif isinstance(obj, BioCPassage):
        yield from obj.sentences
    else:
        raise TypeError(f'Object of type {obj.__class__.__name__} must be BioCCollection, '
                        f'BioCDocument, BioCPassage, or BioCSentence')
