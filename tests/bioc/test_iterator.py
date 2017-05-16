import os
import pytest

from ..context import bioc


def test_sentences():
    filename = os.path.join(os.path.dirname(__file__), 'everything.xml')
    with open(filename) as fp:
        collection = bioc.load(fp)

    sentences = list(bioc.sentences(collection))
    assert 2 == len(sentences)
    assert 27 == sentences[0].offset
    assert 34 == sentences[1].offset

    with pytest.raises(ValueError):
        next(bioc.sentences('Foo'))


def test_annotations():
    filename = os.path.join(os.path.dirname(__file__), 'everything.xml')
    with open(filename) as fp:
        collection = bioc.load(fp)

    annotations = list(bioc.annotations(collection))
    assert 2 == len(annotations)
    assert '1' == annotations[0].id
    assert '2' == annotations[1].id

    annotations = list(bioc.annotations(collection, level=bioc.SENTENCE))
    assert 2 == len(annotations)
    assert '3' == annotations[0].id
    assert '4' == annotations[1].id

    with pytest.raises(ValueError):
        next(bioc.annotations('Foo'))


def test_relations():
    filename = os.path.join(os.path.dirname(__file__), 'everything.xml')
    with open(filename) as fp:
        collection = bioc.load(fp)

    relations = list(bioc.relations(collection))
    assert 1 == len(relations)
    assert 'R1' == relations[0].id

    relations = list(bioc.relations(collection, level=bioc.SENTENCE))
    assert 1 == len(relations)
    assert 'R3' == relations[0].id

    relations = list(bioc.relations(collection, level=bioc.DOCUMENT))
    assert 1 == len(relations)
    assert 'R2' == relations[0].id

    with pytest.raises(ValueError):
        next(bioc.relations('Foo'))
