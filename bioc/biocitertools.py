from typing import Generator

from bioc import BioCCollection, BioCDocument, BioCPassage, BioCSentence, BioCAnnotation, BioCRelation

DOCUMENT = 1
PASSAGE = 2
SENTENCE = 3


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
            for ann in annotations(document, level=level):
                yield ann
    elif isinstance(obj, BioCDocument):
        if level == DOCUMENT:
            for ann in obj.annotations:
                yield ann
        elif level == PASSAGE or level == SENTENCE:
            for passage in obj.passages:
                for ann in annotations(passage, level=level):
                    yield ann
        else:
            raise ValueError('level must be DOCUMENT, PASSAGE, or SENTENCE')
    elif isinstance(obj, BioCPassage):
        if level == PASSAGE:
            for ann in obj.annotations:
                yield ann
        elif level == SENTENCE:
            for sentence in obj.sentences:
                for ann in annotations(sentence, level=level):
                    yield ann
        else:
            raise ValueError('level must be SENTENCE')
    elif isinstance(obj, BioCSentence):
        if level == SENTENCE:
            for ann in obj.annotations:
                yield ann
        else:
            raise ValueError('level must be SENTENCE')
    else:
        raise ValueError('obj must be BioCCollection, BioCDocument, BioCPassage, or BioCSentence')


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
            for rel in relations(document, level=level):
                yield rel
    elif isinstance(obj, BioCDocument):
        if level == DOCUMENT:
            for rel in obj.relations:
                yield rel
        elif level == PASSAGE or level == SENTENCE:
            for passage in obj.passages:
                for rel in relations(passage, level=level):
                    yield rel
        else:
            raise ValueError('level must be DOCUMENT, PASSAGE, or SENTENCE')
    elif isinstance(obj, BioCPassage):
        if level == PASSAGE:
            for rel in obj.relations:
                yield rel
        elif level == SENTENCE:
            for sentence in obj.sentences:
                for rel in relations(sentence, level=level):
                    yield rel
        else:
            raise ValueError('level must be SENTENCE')
    elif isinstance(obj, BioCSentence):
        if level == SENTENCE:
            for rel in obj.relations:
                yield rel
        else:
            raise ValueError('level must be SENTENCE')
    else:
        raise ValueError('obj must be BioCCollection, BioCDocument, BioCPassage, or BioCSentence')


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
            for sentence in sentences(document):
                yield sentence
    elif isinstance(obj, BioCDocument):
        for passage in obj.passages:
            for sentence in sentences(passage):
                yield sentence
    elif isinstance(obj, BioCPassage):
        for sentence in obj.sentences:
            yield sentence
    else:
        raise ValueError('obj must be BioCCollection, BioCDocument, or BioCPassage')
