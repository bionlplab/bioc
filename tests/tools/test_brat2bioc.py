import pytest

from bioc import brat
from bioc.tools.brat2bioc import brat2bioc

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
    return brat.loads(txt_text, ann_text)


def test_brat2bioc(document):
    c = brat2bioc([document])
    assert len(c.documents) == 1

    d = c.documents[0]
    assert d.text == txt_text
    assert len(d.annotations) == 3
    assert len(d.relations) == 3
