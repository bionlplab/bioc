"""
Utilities
"""
from typing import Tuple

from lxml import etree

import bioc


def pad_char(text: str, width: int, char: str = '\n') -> str:
    """Pads a text until length width."""
    dis = width - len(text)
    if dis < 0:
        raise ValueError
    if dis > 0:
        text += char * dis
    return text


def get_text(obj) -> Tuple[int, str]:
    """
    Return text with its offset in the document

    Args:
        obj: BioCDocument, BioCPassage, or BioCSentence

    Returns:
        offset, text
    """
    from bioc.bioc import BioCDocument, BioCPassage, BioCSentence

    if isinstance(obj, BioCSentence):
        return obj.offset, obj.text
    elif isinstance(obj, BioCPassage):
        if obj.text:
            return obj.offset, obj.text
        text = ''
        for sentence in obj.sentences:
            try:
                text = pad_char(text, sentence.offset - obj.offset, ' ')
                assert sentence.text, f'BioC sentence has no text: {sentence.offset}'
                text += sentence.text
            except ValueError:
                raise ValueError(f'Overlapping sentences {sentence.offset}')
        return obj.offset, text
    elif isinstance(obj, BioCDocument):
        text = ''
        for passage in obj.passages:
            try:
                text = pad_char(text, passage.offset)
                text += get_text(passage)[1]
            except ValueError:
                raise ValueError(f'{obj.id}: overlapping passages {passage.offset}')
        return 0, text
    else:
        raise TypeError(f'Object of type {obj.__class__.__name__} must be BioCCollection, '
                        f'BioCDocument, BioCPassage, or BioCSentence')


def pretty_print(src, dst):
    """
    Pretty print the XML file
    """
    parser = etree.XMLParser(remove_blank_text=True)
    if not isinstance(src, str):
        src = str(src)
    tree = etree.parse(src, parser)
    docinfo = tree.docinfo
    with open(dst, 'wb') as fp:
        fp.write(etree.tostring(tree, pretty_print=True,
                                encoding=docinfo.encoding, standalone=docinfo.standalone))


def shorten_text(text: str):
    """Return a short repr of text if it is longer than 40"""
    if len(text) <= 40:
        text = text
    else:
        text = text[:17] + ' ... ' + text[-17:]
    return repr(text)
