"""
Validate Brat data structure
"""
from typing import Callable, List

from bioc.brat.brat import BratDocument, BratEntity


def _default_error(msg: str):
    """Default error handler that accepts two parameters: error message and traceback."""
    raise ValueError(msg)


def validate(document: BratDocument, onerror: Callable[[str], None]= _default_error):
    """Validate a single document."""
    for ann in document.entities:
        anntext = ''
        for span in sorted(ann.locations, key=lambda s: s[0]):
            anntext += document.text[span[0]: span[1]]
        if anntext != ann.text:
            onerror(
                '%s: Annotation text is incorrect at %d.\n'
                '  Annotation: %r\n'
                '  Actual text: %r' %
                (document.id, ann.total_span[0], anntext, ann.text))

    for rel in document.relations:
        for arg_id in rel.arguments.values():
            if not document.has_annotation_id(arg_id):
                onerror('%s: Cannot find id %s' % (document.id, arg_id))

    for event in document.events:
        if not document.has_annotation_id(event.trigger_id):
            _default_error('%s: Cannot find id %s' % (document.id, event.trigger_id))
        for arg_id in event.arguments.values():
            if not document.has_annotation_id(arg_id):
                onerror('%s: Cannot find id %s' % (document.id, arg_id))

    for att in document.attributes:
        if not document.has_annotation_id(att.refid):
            onerror('%s: Cannot find id %s' % (document.id, att.refid))

    for rel in document.equiv_relations:
        for arg_id in rel.argids:
            if not document.has_annotation_id(arg_id):
                onerror('%s: Cannot find id %s' % (document.id, arg_id))

    for note in document.notes:
        if not document.has_annotation_id(note.refid):
            onerror('%s: Cannot find id %s' % (document.id, note.refid))
