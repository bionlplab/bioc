from bioc import bioc


def test_relation():
    base = bioc.BioCRelation()
    base.id = 'R1'
    base.infons['key1'] = 'value1'
    base.add_node(bioc.BioCNode('1', 'role1'))
    base.add_node(bioc.BioCNode('2', 'role2'))
    assert base.get_node('role1').refid == '1'
    assert base.get_node('role3') is None