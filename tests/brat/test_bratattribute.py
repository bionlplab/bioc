from bioc.brat.brat import BratAttribute
from bioc.brat.decoder import loads_brat_attribute
from bioc.brat.encoder import dumps_brat_attribute


def get_attr(id, type, refid, attributes):
    a = BratAttribute()
    a.id = id
    a.type = type
    a.refid = refid
    for att in attributes:
        a.add_attribute(att)
    return a


def test_attribute():
    base = get_attr('A1', 'type', 'E1', ['L1'])
    actual = get_attr('A1', 'type', 'E1', ['L1'])
    assert base == actual

    diff = get_attr('A2', 'type', 'E1', ['L1'])
    assert base != diff

    diff = get_attr('A1', 'type2', 'E1', ['L1'])
    assert base != diff

    diff = get_attr('A1', 'type', 'E2', ['L1'])
    assert base != diff

    diff = get_attr('A1', 'type', 'E1', ['L1', 'L2'])
    assert base != diff

    line = 'A1\ttype E1 L1'
    actual = loads_brat_attribute(line)
    assert base == actual

    assert line == dumps_brat_attribute(base)

