from pathlib import Path

import pytest

import bioc

file = Path(__file__).parent / 'everything.xml'
with open(file, encoding='utf8') as fp:
    collection = bioc.load(fp)


def test_sentences():
    sentences = list(bioc.sentences(collection))
    assert 2 == len(sentences)
    assert 27 == sentences[0].offset
    assert 34 == sentences[1].offset

    with pytest.raises(ValueError):
        next(bioc.sentences('Foo'))


def test_annotations():
    annotations = list(bioc.annotations(collection))
    assert 2 == len(annotations)
    assert '1' == annotations[0].id
    assert '2' == annotations[1].id

    annotations = list(bioc.annotations(collection, level=bioc.SENTENCE))
    assert 2 == len(annotations)
    assert '3' == annotations[0].id
    assert '4' == annotations[1].id

    annotations = list(bioc.annotations(collection, level=bioc.DOCUMENT))
    assert 1 == len(annotations)
    assert '5' == annotations[0].id

    with pytest.raises(ValueError):
        next(bioc.annotations('Foo'))

    with pytest.raises(ValueError):
        next(bioc.annotations(collection, level=-1))

    with pytest.raises(ValueError):
        next(bioc.annotations(collection.documents[0].passages[0], level=bioc.DOCUMENT))

    with pytest.raises(ValueError):
        next(bioc.annotations(collection.documents[1].passages[0].sentences[0], level=bioc.DOCUMENT))
        next(bioc.annotations(collection.documents[1].passages[0].sentences[0], level=bioc.PASSAGE))


def test_relations():
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

    with pytest.raises(ValueError):
        next(bioc.relations(collection, level=-1))

    with pytest.raises(ValueError):
        next(bioc.relations(collection.documents[0].passages[0], level=bioc.DOCUMENT))

    with pytest.raises(ValueError):
        next(bioc.relations(collection.documents[1].passages[0].sentences[0], level=bioc.DOCUMENT))
        next(bioc.relations(collection.documents[1].passages[0].sentences[0], level=bioc.PASSAGE))

