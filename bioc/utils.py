"""
Utilities
"""
from typing import Tuple

from lxml import etree

from bioc import BioCDocument, BioCPassage, BioCSentence


def pad_char(text: str, width: int, char: str = '\n') -> str:
    """Pads a text until length width."""
    dis = width - len(text)
    if dis < 0:
        raise ValueError
    if dis > 0:
        text += char * dis
    return text


def get_text(obj: BioCDocument or BioCPassage or BioCSentence) -> Tuple[int, str]:
    """
    Return text with its offset in the document

    Args:
        obj: BioCDocument, BioCPassage, or BioCSentence

    Returns:
        offset, text
    """
    if isinstance(obj, BioCSentence):
        return obj.offset, obj.text
    if isinstance(obj, BioCPassage):
        if obj.text:
            return obj.offset, obj.text
        text = ''
        for sentence in obj.sentences:
            try:
                text = pad_char(text, sentence.offset - obj.offset, ' ')
                assert sentence.text, f'BioC sentence has no text: {sentence.offset}'
                text += sentence.text
            except:
                raise ValueError(f'Overlapping sentences {sentence.offset}')
        return obj.offset, text
    if isinstance(obj, BioCDocument):
        text = ''
        for passage in obj.passages:
            try:
                text = pad_char(text, passage.offset)
                text += get_text(passage)[1]
            except:
                raise ValueError(f'{obj.id}: overlapping passages {passage.offset}')
        return 0, text
    raise TypeError(f'Object of type {obj.__class__.__name__} must be BioCCollection, '
                    f'BioCDocument, BioCPassage, or BioCSentence')


def pretty_print(source, dest):
    """
    Pretty print the XML file
    """
    parser = etree.XMLParser(remove_blank_text=True)
    if not isinstance(source, str):
        source = str(source)
    tree = etree.parse(source, parser)
    docinfo = tree.docinfo
    with open(dest, 'wb') as fp:
        fp.write(etree.tostring(tree, pretty_print=True,
                                encoding=docinfo.encoding, standalone=docinfo.standalone))
