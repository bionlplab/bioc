import copy
from pathlib import Path

import pytest

from bioc import biocxml
import bioc


@pytest.fixture
def collection():
    file = Path(__file__).parent / 'everything.xml'
    with open(file, encoding='utf8') as fp:
        collection = biocxml.load(fp)
    return collection


def test_AnnotationMixin(collection):
    c = copy.deepcopy(collection)
    p = c.documents[0].passages[0]

    p.clear_annotations()
    assert len(p.annotations) == 0
    p.clear_relations()
    assert len(p.relations) == 0

    c = copy.deepcopy(collection)
    p = c.documents[0].passages[0]

    ann = p.get_annotation('1')
    assert ann.total_span.offset == 1

    ann = p.get_annotation('2')
    assert ann.total_span.offset == 5

    rel = p.get_relation('R1')
    assert rel.infons['relation-infon-key'] == 'relation-infon-value'

    ann = p.get('1')
    assert ann.total_span.offset == 1

    rel = p.get('R1')
    assert rel.infons['relation-infon-key'] == 'relation-infon-value'

    with pytest.raises(KeyError):
        p.get('x')

    with pytest.raises(KeyError):
        p.get_annotation('x')

    with pytest.raises(KeyError):
        p.get_relation('x')


def test_BioCPassage(collection):
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


def test_BioCDocument(collection):
    d = collection.documents[0]
    assert d.get_passage(0).text == 'abcdefghijklmnopqrstuvwxyz'
    assert d.get_passage(10) is None

    text = 'abcdefghijklmnopqrstuvwxyz'
    doc = bioc.BioCDocument.of_text(text)
    assert doc.text == text

    passages = d.passages
    newd = bioc.BioCDocument.of_passages(*passages)
    for p1, p2 in zip(newd.passages, d.passages):
        assert p1.text == p2.text

    with pytest.raises(ValueError):
        bioc.BioCDocument.of_passages()

    with pytest.raises(ValueError):
        bioc.BioCDocument.of_passages(None)


def test_BioCColection(collection):
    documents = collection.documents
    newc = bioc.BioCCollection.of_documents(*documents)

    for d1, d2 in zip(newc.documents, collection.documents):
        assert d1.id == d2.id

    with pytest.raises(ValueError):
        bioc.BioCCollection.of_documents()

    with pytest.raises(ValueError):
        bioc.BioCCollection.of_documents(None)
