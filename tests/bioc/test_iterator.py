from pathlib import Path

import pytest

import bioc
from bioc import DOCUMENT, PASSAGE, SENTENCE

file = Path(__file__).parent / 'everything_v2.xml'
with open(file, encoding='utf8') as fp:
    collection = bioc.load(fp, version=bioc.BioCVersion.V2)


def test_sentences():
    results = list(bioc.sentences(collection))
    assert 2 == len(results)
    assert 27 == results[0].sentence.offset
    assert 27 == results[0].passage.offset
    assert '2' == results[0].document.id

    assert 34 == results[1].sentence.offset
    assert 27 == results[1].passage.offset
    assert '2' == results[1].document.id

    with pytest.raises(TypeError):
        next(bioc.sentences('Foo'))


def test_annotations():
    results = list(bioc.annotations(collection))
    assert {'1', '2', '3', '4', '5'} == {r.annotation.id for r in results}

    results = list(bioc.annotations(collection, level=DOCUMENT))
    assert {'5'} == {r.annotation.id for r in results}
    assert {'1'} == {r.document.id for r in results}
    assert {None} == {r.passage for r in results}

    results = list(bioc.annotations(collection, level=PASSAGE))
    assert {'1', '2'} == {r.annotation.id for r in results}
    assert {'1'} == {r.document.id for r in results}
    assert {0} == {r.passage.offset for r in results}
    assert {None} == {r.sentence for r in results}

    results = list(bioc.annotations(collection, level=SENTENCE))
    assert {'3', '4'} == {r.annotation.id for r in results}
    assert {'2'} == {r.document.id for r in results}
    assert {27} == {r.passage.offset for r in results}
    assert {27, 34} == {r.sentence.offset for r in results}

    results = list(bioc.annotations(collection.documents[0], level=SENTENCE))
    assert len(results) == 0

    with pytest.raises(TypeError):
        next(bioc.annotations('Foo'))


def test_relations():
    results = list(bioc.relations(collection))
    assert {'R1', 'R2', 'R3'} == {r.relation.id for r in results}

    results = list(bioc.relations(collection, level=DOCUMENT))
    assert {'R2'} == {r.relation.id for r in results}
    assert {'1'} == {r.document.id for r in results}
    assert {None} == {r.passage for r in results}

    results = list(bioc.relations(collection, level=PASSAGE))
    assert {'R1'} == {r.relation.id for r in results}
    assert {'1'} == {r.document.id for r in results}
    assert {0} == {r.passage.offset for r in results}
    assert {None} == {r.sentence for r in results}

    results = list(bioc.relations(collection, level=SENTENCE))
    assert {'R3'} == {r.relation.id for r in results}
    assert {'2'} == {r.document.id for r in results}
    assert {27} == {r.passage.offset for r in results}
    assert {27} == {r.sentence.offset for r in results}

    with pytest.raises(TypeError):
        next(bioc.relations('Foo'))
