import copy
from pathlib import Path

import pytest

from bioc import biocxml, bioc

file = Path(__file__).parent / 'everything.xml'
with open(file, encoding='utf8') as fp:
    collection = biocxml.load(fp)


def test_BioCLocation():
    base = bioc.BioCLocation(1, 10)
    assert base != 'foo'
    assert base.end == 11

    loc = bioc.BioCLocation(1, 10)
    assert base == loc

    loc = bioc.BioCLocation(2, 9)
    assert base != loc
    assert loc in base
    assert base not in loc

    locs = {base, loc}
    assert base in locs
    assert loc in locs

    with pytest.raises(TypeError):
        assert 'foo' in base


def test_BioCNode():
    base = bioc.BioCNode('refid', 'role')
    assert base != 'foo'

    node = bioc.BioCNode('refid', 'role')
    assert base == node

    node = bioc.BioCNode('refid', 'role2')
    assert base != node

    nodes = {base, node}
    assert base in nodes
    assert node in nodes


def test_BioCAnnotation():
    base = bioc.BioCAnnotation()
    base.add_location(bioc.BioCLocation(1, 10))

    ann = bioc.BioCAnnotation()
    ann.add_location(bioc.BioCLocation(2, 9))

    assert ann in base
    assert base not in ann

    with pytest.raises(TypeError):
        assert 'foo' in base

    with pytest.raises(ValueError):
        del base.locations[:]
        assert base.total_span


def test_BioCRelation():
    base = collection.documents[0].passages[0].relations[0]
    assert base.get_node('role1').refid == '1'
    assert base.get_node('role3') is None


def test_InfonsMaxin():
    c = copy.deepcopy(collection)
    c.clear_infons()
    assert len(c.infons) == 0


def test_AnnotationMixin():
    c = copy.deepcopy(collection)
    p = c.documents[0].passages[0]
    p.clear_annotations()
    assert len(p.annotations) == 0
    p.clear_relations()
    assert len(p.relations) == 0


def test_BioCPassage():
    p = collection.documents[1].passages[0]
    assert p.get_sentence(34).text == '测试Non-ASCII'
    assert p.get_sentence(10) is None

    sentences = p.sentences
    newp = bioc.BioCPassage.of_sentences(*sentences)
    for s1, s2 in zip(newp.sentences, p.sentences):
        assert s1.text == s2.text

    with pytest.raises(ValueError):
        bioc.BioCPassage.of_sentences()

    with pytest.raises(ValueError):
        bioc.BioCPassage.of_sentences(None)

    p = collection.documents[0].passages[0]
    p_copy = bioc.BioCPassage.of_text(p.text, p.offset)
    assert p.text == p_copy.text
    assert p.offset == p_copy.offset


def test_BioCSentence():
    s = collection.documents[1].passages[0].sentences[0]
    s_copy = bioc.BioCSentence.of_text(s.text, s.offset)
    assert s.text == s_copy.text
    assert s.offset == s_copy.offset


def test_BioCDocument():
    d = collection.documents[0]
    assert d.get_passage(0).text == 'abcdefghijklmnopqrstuvwxyz'
    assert d.get_passage(10) is None

    text = 'abcdefghijklmnopqrstuvwxyz'
    doc = bioc.BioCDocument.of_text(text)
    assert doc.get_passage(0).text == text

    passages = d.passages
    newd = bioc.BioCDocument.of_passages(*passages)
    for p1, p2 in zip(newd.passages, d.passages):
        assert p1.text == p2.text

    with pytest.raises(ValueError):
        bioc.BioCDocument.of_passages()

    with pytest.raises(ValueError):
        bioc.BioCDocument.of_passages(None)


def test_BioCColection():
    documents = collection.documents
    newc = bioc.BioCCollection.of_documents(*documents)

    for d1, d2 in zip(newc.documents, collection.documents):
        assert d1.id == d2.id

    with pytest.raises(ValueError):
        bioc.BioCCollection.of_documents()

    with pytest.raises(ValueError):
        bioc.BioCCollection.of_documents(None)
