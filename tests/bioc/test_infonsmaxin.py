from bioc.datastructure import InfonsMaxin


def test_infonsmaxin():
    c = InfonsMaxin()
    for i in range(0, 10):
        c.infons[str(i)] = str(i)
    assert len(c.infons) == 10

    c.clear_infons()
    assert len(c.infons) == 0

    c.infons['k1'] = 'v1'
    c.infons['k2'] = 'v2'
    assert c.infons_repr() == 'infons=[k1=v1,k2=v2],'

