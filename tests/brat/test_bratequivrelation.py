from bioc.brat.brat import BratEquivRelation
from bioc.brat.decoder import loads_brat_equiv
from bioc.brat.encoder import dumps_brat_equiv


def get_relation(arguments):
    r = BratEquivRelation()
    for id in arguments:
        r.add_argid(id)
    return r


def test_relation():
    base = get_relation(['T1'])
    assert base != 1

    actual = get_relation(['T1'])
    assert base == actual

    diff = get_relation(['T1', 'T2'])
    assert base != diff

    base = get_relation(['T1', 'T2'])
    line = '*\tEquiv T1 T2'
    actual = loads_brat_equiv(line)
    assert base == actual

    assert line == dumps_brat_equiv(base)
