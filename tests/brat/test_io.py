from bioc.brat import decoder, encoder


ann_text = """
T1	Protein 48 53	BMP-6
T2	Protein 161 164	Id1
T3	Protein 202 207	BMP-6
T4	Protein 321 326	CD40L
T5	Protein 342 347	BMP-6
T6	Protein 493 498	BMP-6
T7	Positive_regulation 135 146	consecutive
T8	Gene_expression 147 157	production
E1	Positive_regulation:T7 Theme:E2
E2	Gene_expression:T8 Theme:T2
R1	PPI Arg1:T1 Arg2:T2
A1	Negation E1
*	Equiv T1 T2

#1	AnnotatorNotes T1	this annotation is suspect
"""


def test_decoder():
    document = decoder.loads(ann_text)
    assert len(document.entities) == 8
    assert len(document.events) == 2
    assert len(document.relations) == 1
    assert len(document.attributes) == 1
    assert len(document.equiv_relations) == 1
    assert len(document.notes) == 1


def test_load(tmp_path):
    filepath = tmp_path / 'foo.ann'
    with open(filepath, 'w') as fp:
        fp.write(ann_text)

    with open(filepath) as fp:
        document = decoder.load(fp)

    assert len(document.entities) == 8
    assert len(document.events) == 2
    assert len(document.relations) == 1
    assert len(document.attributes) == 1
    assert len(document.equiv_relations) == 1
    assert len(document.notes) == 1


def test_dumps():
    base = decoder.loads(ann_text)
    s = encoder.dumps(base)
    document = decoder.loads(s)
    assert len(document.entities) == 8
    assert len(document.events) == 2
    assert len(document.relations) == 1
    assert len(document.attributes) == 1
    assert len(document.equiv_relations) == 1
    assert len(document.notes) == 1


def test_dump(tmp_path):
    base = decoder.loads(ann_text)
    filepath = tmp_path / 'foo.ann'
    with open(filepath, 'w') as fp:
        encoder.dump(base, fp)

    with open(filepath) as fp:
        document = decoder.load(fp)

    assert len(document.entities) == 8
    assert len(document.events) == 2
    assert len(document.relations) == 1
    assert len(document.attributes) == 1
    assert len(document.equiv_relations) == 1
    assert len(document.notes) == 1