from bioc.brat import decoder, encoder
from bioc.brat.brat import BratDocument

txt_text = "There is no PPI relation between protein 1 and protein 2."

ann_text = """
T1	Protein 33 42	protein 1
T2	Protein 47 56	protein 2
T3	Trigger 12 15	PPI
R1	PPI Arg1:T1 Arg2:T2
E1	PPI:T3 Arg1:T1 Arg2:T2
A1	Negation E1
*	Equiv T1 T2
#1	AnnotatorNotes T1	this annotation is suspect
"""


def _assert(document: BratDocument):
    assert len(document.entities) == 3
    assert len(document.events) == 1
    assert len(document.relations) == 1
    assert len(document.attributes) == 1
    assert len(document.equiv_relations) == 1
    assert len(document.notes) == 1
    assert document.has_annotation_id('T1')


def test_loads():
    document = decoder.loads(txt_text, ann_text)
    _assert(document)


def test_load(tmp_path):
    annpath = tmp_path / 'foo.ann'
    txtpath = tmp_path / 'foo.txt'

    with open(annpath, 'w') as fp:
        fp.write(ann_text)
    with open(txtpath, 'w') as fp:
        fp.write(txt_text)

    with open(annpath) as ann_fp, open(txtpath) as txt_fp:
        document = decoder.load(txt_fp, ann_fp)

    _assert(document)


def test_dumps():
    base = decoder.loads_ann(ann_text)
    s = encoder.dumps_ann(base)
    document = decoder.loads_ann(s)
    _assert(document)


def test_dump(tmp_path):
    annpath = tmp_path / 'foo.ann'
    txtpath = tmp_path / 'foo.txt'

    base = decoder.loads(txt_text, ann_text)
    with open(annpath, 'w') as ann_fp, open(txtpath, 'w') as text_fp:
        encoder.dump(base, text_fp, ann_fp)

    with open(annpath) as ann_fp, open(txtpath) as text_fp:
        document = decoder.load(text_fp, ann_fp)

    _assert(document)


def test_loaddir(tmp_path):
    for i in range(10):
        with open(tmp_path / f'{i}.txt', 'w') as fp:
            fp.write(txt_text)
        with open(tmp_path / f'{i}.ann', 'w') as fp:
            fp.write(ann_text)
        with open(tmp_path / f'{i}.a1', 'w') as fp:
            fp.write(ann_text)
        with open(tmp_path / f'{i}.a2', 'w') as fp:
            fp.write(ann_text)
    docs = decoder.loaddir(tmp_path)
    assert len(docs) == 10

    docs = [doc for doc in decoder.iterloaddir(tmp_path, ann_file=False)]
    assert len(docs) == 10