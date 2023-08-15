from bioc.brat import BratEntity, BratDocument


def get_entity(id, type, text, spans):
    e = BratEntity()
    e.id = id
    e.type = type
    e.text = text
    for span in spans:
        e.add_span(span[0], span[1])
    return e


def test_entity():
    doc = BratDocument()
    e1 = get_entity('T1', 'type1', 'text1', [(48, 53)])
    doc.add_annotation(e1)

    e2 = get_entity('T2', 'type2', 'text2', [(48, 53)])
    doc.add_annotation(e2)

    ann = doc.get_annotation('T1')
    assert ann == e1

    ann = doc.get_annotation('T3')
    assert ann is None
