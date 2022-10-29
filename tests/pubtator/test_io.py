import pytest

from bioc import pubtator

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
8701013	CID	D015738	D014456	No
"""


text2 = """
22051099|t|Variation in the CXCR1 gene (IL8RA) is not associated with susceptibility to chronic periodontitis.
22051099|a|BACKGROUND: The chemokine receptor 1 CXCR-1 (or IL8R-alpha) is a specific receptor for the interleukin 8 (IL-8), which is chemoattractant for neutrophils and has an important role in the inflammatory response. The polymorphism rs2234671 at position Ex2+860G>C of the CXCR1 gene causes a conservative amino acid substitution (S276T). This single nucleotide polymorphism (SNP) seemed to be functional as it was associated with decreased lung cancer risk. Previous studies of our group found association of haplotypes in the IL8 and in the CXCR2 genes with the multifactorial disease chronic periodontitis. In this study we investigated the polymorphism rs2234671 in 395 Brazilian subjects with and without chronic periodontitis. FINDINGS: Similar distribution of the allelic and genotypic frequencies were observed between the groups (p>0.05). CONCLUSIONS: The polymorphism rs2234671 in the CXCR1 gene was not associated with the susceptibility to chronic periodontitis in the studied Brazilian population.
22051099	327	336	rs2234671	SNP	rs2234671
22051099	349	359	Ex2+860G>C	DNAMutation	c|SUB|G|Ex2+860|C	RSID:2234671
22051099	425	430	S276T	ProteinMutation	p|SUB|S|276|T	RSID:2234671
22051099	751	760	rs2234671	SNP	rs2234671
22051099	972	981	rs2234671	SNP	rs2234671
"""


def _test_doc(doc):
    assert len(doc.relations) == 2
    assert len(doc.annotations) == 11
    assert doc.annotations[0].id == 'D015738'
    assert doc.annotations[-1].type == 'Chemical'


def _test_doc2(doc):
    assert len(doc.relations) == 0
    assert len(doc.annotations) == 5
    assert doc.annotations[1].id == 'c|SUB|G|Ex2+860|C'
    assert doc.annotations[1].others == ['RSID:2234671']


def test_loads():
    docs = pubtator.loads(text)
    assert len(docs) == 1
    _test_doc(docs[0])

    docs = pubtator.loads(text2)
    assert len(docs) == 1
    _test_doc2(docs[0])


def test_load(tmp_path):
    filepath = tmp_path / 'foo.txt'
    with open(filepath, 'w') as fp:
        fp.write(text)
    with open(filepath) as fp:
        docs = pubtator.load(fp)
    assert len(docs) == 1
    _test_doc(docs[0])


def test_iterparse(tmp_path):
    filepath = tmp_path / 'foo.txt'
    with open(filepath, 'w') as fp:
        fp.write(text)
        fp.write('\n')
        fp.write(text)

    with open(filepath) as fp:
        docs = [doc for doc in pubtator.iterparse(fp)]

    assert len(docs) == 2
    _test_doc(docs[0])
    _test_doc(docs[1])


def test_loads_ann():
    text = "23949582\t297\t317\themorrhagic cystitis\tDisease\tD006470|D003556\themorrhagic|cystitis"
    ann = pubtator.loads_ann(text)
    assert ann.text == 'hemorrhagic cystitis'

    with pytest.raises(ValueError):
        text = "23949582\t297\t317\themorrhagic cystitis\tDisease\tD006470|D003556\themorrhagic|cystitis|ABC"
        pubtator.loads_ann(text)

    with pytest.raises(ValueError):
        text = "23949582\t297\t317"
        pubtator.loads_ann(text)


def test_dump(tmp_path):
    docs = pubtator.loads(text)
    filepath = tmp_path / 'foo.txt'
    with open(filepath, 'w') as fp:
        pubtator.dump(docs, fp)
    with open(filepath) as fp:
        docs = pubtator.load(fp)
    assert len(docs) == 1
    _test_doc(docs[0])


def test_dumps():
    docs = pubtator.loads(text)
    s = pubtator.dumps(docs)
    docs = pubtator.loads(s)
    assert len(docs) == 1
    _test_doc(docs[0])
