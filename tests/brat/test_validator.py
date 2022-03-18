import pytest

from bioc.brat import decoder
from bioc.brat.validator import validate

txt_text = "There is no PPI relation between protein 1 and protein 2."

ann_text = """
T1	Protein 33 40;41 42	protein1
T2	Protein 47 56	protein 2
T3	Trigger 12 15	PPI
R1	PPI Arg1:T1 Arg2:T2
E1	PPI:T3 Arg1:T1 Arg2:T2
A1	Negation E1
*	Equiv T1 T2
#1	AnnotatorNotes T1	this annotation is suspect
"""

@pytest.fixture
def document():
    return decoder.loads(txt_text, ann_text)


def test_validate(document):
    validate(document)


def test_entity_error(document):
    with pytest.raises(ValueError):
        document.entities[0].text = ''
        validate(document)


def test_event_error(document):
    with pytest.raises(ValueError):
        document.events[0].trigger_id = 'T4'
        validate(document)


def test_event2_error(document):
    with pytest.raises(ValueError):
        document.events[0].arguments['Arg1'] = 'T4'
        validate(document)


def test_rel_error(document):
    with pytest.raises(ValueError):
        document.relations[0].arguments['Arg1'] = 'T4'
        validate(document)


def test_att_error(document):
    with pytest.raises(ValueError):
        document.attributes[0].refid = 'T4'
        validate(document)


def test_note_error(document):
    with pytest.raises(ValueError):
        document.notes[0].refid = 'T4'
        validate(document)


def test_equiv_error(document):
    with pytest.raises(ValueError):
        document.equiv_relations[0].argids = {'T4'}
        validate(document)