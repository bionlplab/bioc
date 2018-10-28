from typing import Tuple

import lxml.etree as etree

from bioc import BioCDocument, BioCPassage, BioCSentence


def fill_char(text: str, offset: int, char: str = '\n') -> str:
    dis = offset - len(text)
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
        return obj.offset, obj.text,
    elif isinstance(obj, BioCPassage):
        if obj.text:
            return obj.offset, obj.text
        else:
            text = ''
            for sentence in obj.sentences:
                try:
                    text = fill_char(text, sentence.offset - obj.offset, ' ')
                    assert sentence.text, 'BioC sentence has no text: {}'.format(sentence.offset)
                    text += sentence.text
                except:
                    raise ValueError('Overlapping sentences %d' % (sentence.offset))
            return obj.offset, text
    elif isinstance(obj, BioCDocument):
        text = ''
        for passage in obj.passages:
            try:
                text = fill_char(text, passage.offset)
                text += get_text(passage)[1]
            except:
                raise ValueError('%s: overlapping passages %d' % (obj.id, passage.offset))
        return 0, text
    else:
        raise ValueError('obj must be BioCCollection, BioCDocument, BioCPassage, or BioCSentence')


def pretty_print(src: str, dst: str):
    """
    Pretty print the XML file
    """
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(src, parser)
    docinfo = tree.docinfo
    with open(dst, 'wb') as fp:
        fp.write(etree.tostring(tree, pretty_print=True,
                                encoding=docinfo.encoding, standalone=docinfo.standalone))
