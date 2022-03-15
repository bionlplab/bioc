import pytest

import bioc


def test_location():
    base = bioc.BioCLocation(1, 10)
    assert base != 'foo'
    assert base.end == 11
    assert base.contains(9)
    assert not base.contains(11)

    loc = bioc.BioCLocation(1, 10)
    assert base == loc

    loc = bioc.BioCLocation(2, 9)
    assert base != loc
    assert loc in base
    assert base not in loc

    locs = {base, loc}
    assert base in locs
    assert loc in locs

    with pytest.raises(TypeError):
        assert 'foo' in base