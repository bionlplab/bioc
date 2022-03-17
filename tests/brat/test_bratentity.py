from bioc.brat.brat import BratEntity
from bioc.brat.decoder import loads_brat_entity
from bioc.brat.encoder import dumps_brat_entity


def get_entity(id, type, text, spans):
    e = BratEntity()
    e.id = id
    e.type = type
    e.text = text
    for span in spans:
        e.add_span(span[0], span[1])
    return e


def test_entity():
    base = get_entity('T1', 'type', 'text', [(48, 53)])
    assert base != 1

    actual = get_entity('T1', 'type', 'text', [(48, 53)])
    assert base == actual

    diff = get_entity('T2', 'type', 'text', [(48, 53)])
    assert base != diff

    diff = get_entity('T1', 'type2', 'text', [(48, 53)])
    assert base != diff

    diff = get_entity('T1', 'type', 'text2', [(48, 53)])
    assert base != diff

    diff = get_entity('T1', 'type', 'text', [(48, 53), (56, 57)])
    assert base != diff

    base = get_entity('T1', 'type', 'text', [(48, 53), (56, 57)])
    line = 'T1\ttype 48 53;56 57\ttext'
    actual = loads_brat_entity(line)
    assert base == actual

    assert line == dumps_brat_entity(base)


def test_span():
    base = get_entity('T1', 'type', 'text', [(48, 53), (56, 57)])
    assert base.total_span == (48, 57)


def test_shift():
    base = get_entity('T1', 'type', 'text', [(48, 53), (56, 57)])
    base = base.shit(1)
    assert base.total_span == (49, 58)
