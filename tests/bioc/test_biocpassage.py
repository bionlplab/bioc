import pytest

import bioc


def test_total_span():
    p = bioc.BioCPassage()
    p.offset = 1
    p.text = 'abcdefghijklmnopqrstuvwxyz'

    assert p.total_span == bioc.BioCLocation(1, 26)

    p = bioc.BioCPassage()
    p.offset = 1
    p.add_sentence(bioc.BioCSentence.of_text('1234567890', 1))
    p.add_sentence(bioc.BioCSentence.of_text('abcdefghijklmnopqrstuvwxyz', 50))

    assert p.total_span == bioc.BioCLocation(1, 50 + 26)
