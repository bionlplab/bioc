from bioc.brat.brat import BratEvent
from bioc.brat.decoder import loads_brat_event
from bioc.brat.encoder import dumps_brat_event


def get_event(id, type, trigger_id, arguments):
    r = BratEvent()
    r.id = id
    r.type = type
    r.trigger_id = trigger_id
    for (role, id) in arguments:
        r.add_argument(role, id)
    return r


def test_relation():
    base = get_event('E1', 'type', 'T1', [('Arg1', 'T1')])
    assert base != 1

    actual = get_event('E1', 'type', 'T1', [('Arg1', 'T1')])
    assert base == actual

    diff = get_event('E2', 'type', 'T1', [('Arg1', 'T1')])
    assert base != diff

    diff = get_event('E1', 'type2', 'T1', [('Arg1', 'T1')])
    assert base != diff

    diff = get_event('E1', 'type', 'T2', [('Arg1', 'T1')])
    assert base != diff

    diff = get_event('E1', 'type', 'T1', [('Arg1', 'T1'), ('Arg2', 'T2')])
    assert base != diff

    base = get_event('E1', 'type', 'T1', [('Arg1', 'T1'), ('Arg2', 'T2')])
    line = 'E1\ttype:T1 Arg1:T1 Arg2:T2'
    actual = loads_brat_event(line)
    assert base == actual

    assert line == dumps_brat_event(base)
