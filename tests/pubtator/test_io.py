import pytest

from bioc.pubtator import decoder, encoder

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

def _test_doc(doc):
    assert len(doc.relations) == 1
    assert len(doc.annotations) == 11
    assert doc.annotations[0].id == 'D015738'
    assert doc.annotations[-1].type == 'Chemical'


def test_loads():
    docs = decoder.loads(text)
    assert len(docs) == 1
    _test_doc(docs[0])



def test_load(tmp_path):
    filepath = tmp_path / 'foo.txt'
    with open(filepath, 'w') as fp:
        fp.write(text)
    with open(filepath) as fp:
        docs = decoder.load(fp)
    assert len(docs) == 1
    _test_doc(docs[0])


def test_iterparse(tmp_path):
    filepath = tmp_path / 'foo.txt'
    with open(filepath, 'w') as fp:
        fp.write(text)
        fp.write('\n')
        fp.write(text)

    with open(filepath) as fp:
        docs = [doc for doc in decoder.iterparse(fp)]

    assert len(docs) == 2
    _test_doc(docs[0])
    _test_doc(docs[1])


def test_loads_ann():
    text = "23949582\t297\t317\themorrhagic cystitis\tDisease\tD006470|D003556\themorrhagic|cystitis"
    ann = decoder.loads_ann(text)
    assert ann.text == 'hemorrhagic cystitis'

    with pytest.raises(ValueError):
        text = "23949582\t297\t317\themorrhagic cystitis\tDisease\tD006470|D003556\themorrhagic|cystitis|ABC"
        decoder.loads_ann(text)

    with pytest.raises(ValueError):
        text = "23949582\t297\t317"
        decoder.loads_ann(text)


def test_dump(tmp_path):
    docs = decoder.loads(text)
    filepath = tmp_path / 'foo.txt'
    with open(filepath, 'w') as fp:
        encoder.dump(fp, docs[0])
    with open(filepath) as fp:
        docs = decoder.load(fp)
    assert len(docs) == 1
    _test_doc(docs[0])


def test_dumps():
    docs = decoder.loads(text)
    s = encoder.dumps(docs[0])
    docs = decoder.loads(s)
    assert len(docs) == 1
    _test_doc(docs[0])