import lxml.etree as etree
import bioc


def fill_char(text, offset, char='\n'):
    dis = offset - len(text)
    if dis < 0:
        raise ValueError
    if dis > 0:
        text += char * dis
    return text


def get_text(obj):
    """
    Return text with its offset in the document
    
    Args:
        obj: BioCDocument, BioCPassage, or BioCSentence
    
    Returns:
        tuple(int,str): offset, text
    """
    if isinstance(obj, bioc.BioCSentence):
        return obj.offset, obj.text,
    elif isinstance(obj, bioc.BioCPassage):
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
    elif isinstance(obj, bioc.BioCDocument):
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


def pretty_print(src, dst):
    """
    Pretty print the XML file
    """
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(src, parser)
    docinfo = tree.docinfo
    with open(dst, 'wb') as fp:
        fp.write(etree.tostring(tree, pretty_print=True,
                                encoding=docinfo.encoding, standalone=docinfo.standalone))

