from typing import Callable

from bioc.pubtator.datastructure import PubTator


def _default_error(msg: str):
    """Default error handler that accepts two parameters: error message
    and traceback."""
    raise ValueError(msg)


def validate(obj: PubTator, onerror: Callable[[str], None]= _default_error):
    text = obj.title + '\n' + obj.abstract
    for ann in obj.annotations:
        anntext = text[ann.start:ann.end]
        if anntext != ann.text:
            start = max(0, ann.start - 10)
            end = min(len(text), ann.end + 10)
            onerror(
                '%s: Annotation text is incorrect at %d.\n'
                '  Annotation: %r\n'
                '  Actual text: %r\n'
                '  text: %s' %
                (obj.pmid, ann.start, anntext, ann.text, text[start:end]))
    for rel in obj.relations:
        if obj.get_annotation(rel.id1) is None:
            onerror( '%s: Cannot find %s.' % (obj.pmid, rel.id1))
        if obj.get_annotation(rel.id2) is None:
            onerror('%s: Cannot find %s.' % (obj.pmid, rel.id2))
