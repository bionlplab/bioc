from typing import TextIO

from bioc.pubtator.pubtator import PubTatorAnn, PubTatorRel, PubTator


def dumps_ann(ann: PubTatorAnn) -> str:
    return str(ann)


def dumps_rel(rel: PubTatorRel) -> str:
    return str(rel)


def dumps(doc: PubTator) -> str:
    """
    Serialize obj (an instance of Pubtator) to a Pubtator formatted str.

    Args:
        doc: a Pubtator document

    Return:
        a Pubtator formatted str
    """
    return str(doc)


def dump(fp: TextIO, obj: PubTator):
    """
    Serialize obj (an instance of Pubtator) to file-like object.

    Args:
        fp: a file-like object
        obj: a Pubtator document
    """
    fp.write(dumps(obj) + '\n')
