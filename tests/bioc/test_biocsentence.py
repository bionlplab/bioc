from bioc import bioc


def test_sentence():
    s = bioc.BioCSentence()
    s.offset = 27
    s.text = 'abcdefg'
    s_copy = bioc.BioCSentence.of_text('abcdefg', 27)
    assert s.text == s_copy.text
    assert s.offset == s_copy.offset