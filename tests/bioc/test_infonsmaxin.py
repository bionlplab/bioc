from bioc.bioc.bioc import InfonsMaxin


def test_infonsmaxin():
    c = InfonsMaxin()
    for i in range(0, 10):
        c.infons[str(i)] = str(i)
    assert len(c.infons) == 10

    c.clear_infons()
    assert len(c.infons) == 0