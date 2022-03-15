from bioc.brat.brat import BratRelation
from bioc.brat.decoder import loads_brat_relation
from bioc.brat.encoder import dumps_brat_relation


def get_relation(id, type, arguments):
    r = BratRelation()
    r.id = id
    r.type = type
    for (role, id) in arguments:
        r.add_argument(role, id)
    return r


def test_relation():
    base = get_relation('R1', 'type', [('Arg1', 'T1')])
    actual = get_relation('R1', 'type', [('Arg1', 'T1')])
    assert base == actual

    diff = get_relation('R2', 'type', [('Arg1', 'T1')])
    assert base != diff

    diff = get_relation('R1', 'type2', [('Arg1', 'T1')])
    assert base != diff

    diff = get_relation('R1', 'type', [('Arg1', 'T1'), ('Arg2', 'T2')])
    assert base != diff

    base = get_relation('R1', 'type', [('Arg1', 'T1'), ('Arg2', 'T2')])
    line = 'R1\ttype Arg1:T1 Arg2:T2'
    actual = loads_brat_relation(line)
    assert base == actual

    assert line == dumps_brat_relation(base)
