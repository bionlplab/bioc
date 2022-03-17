from bioc.brat import decoder, encoder
from bioc.brat.brat import BratDocument


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
    assert document.entities[0].id == 'T1'
    assert len(document.events) == 1
    assert len(document.relations) == 1
    assert len(document.attributes) == 1
    assert len(document.equiv_relations) == 1
    assert len(document.notes) == 1


def test_decoder():
    document = decoder.loads_ann(ann_text)
    _assert(document)


def test_load(tmp_path):
    filepath = tmp_path / 'foo.ann'
    with open(filepath, 'w') as fp:
        fp.write(ann_text)

    with open(filepath) as fp:
        document = decoder.load_ann(fp)

    _assert(document)


def test_dumps():
    base = decoder.loads_ann(ann_text)
    s = encoder.dumps_ann(base)
    document = decoder.loads_ann(s)
    _assert(document)


def test_dump(tmp_path):
    base = decoder.loads_ann(ann_text)
    filepath = tmp_path / 'foo.ann'
    with open(filepath, 'w') as fp:
        encoder.dump_ann(base, fp)

    with open(filepath) as fp:
        document = decoder.load_ann(fp)

    _assert(document)