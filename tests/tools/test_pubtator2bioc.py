import pytest

from bioc.bioc.validator import BioCValidator
from bioc import pubtator
from bioc.tools.pubtator2bioc import pubtator2bioc

text = """8701013|t|Famotidine-associated delirium. A series of six cases.
8701013|a|Famotidine is a histamine H2-receptor antagonist used in inpatient settings for prevention of stress ulcers and is showing increasing popularity because of its low cost. Although all of the currently available H2-receptor antagonists have shown the propensity to cause delirium, only two previously reported cases have been associated with famotidine. The authors report on six cases of famotidine-associated delirium in hospitalized patients who cleared completely upon removal of famotidine. The pharmacokinetics of famotidine are reviewed, with no change in its metabolism in the elderly population seen. The implications of using famotidine in elderly persons are discussed.
8701013	0	10	Famotidine	Chemical	D015738
8701013	22	30	delirium	Disease	D003693
8701013	55	65	Famotidine	Chemical	D015738
8701013	156	162	ulcers	Disease	D014456
8701013	324	332	delirium	Disease	D003693
8701013	395	405	famotidine	Chemical	D015738
8701013	442	452	famotidine	Chemical	D015738
8701013	464	472	delirium	Disease	D003693
8701013	537	547	famotidine	Chemical	D015738
8701013	573	583	famotidine	Chemical	D015738
8701013	689	699	famotidine	Chemical	D015738
8701013	CID	D015738	D003693
"""

@pytest.fixture
def documents():
    return pubtator.loads(text)


def test_pubtator2bioc(documents):
    d = pubtator2bioc(documents[0])
    assert len(d.annotations) == 11
    assert len(d.relations) == 1
    # assert d.text[0:10] == 'Famotidine'
    # assert '\n' in d.text
    # assert d.text[689:699] == 'famotidine'
    validator = BioCValidator()
    validator._validate_ann(d.annotations, d.text, 0)