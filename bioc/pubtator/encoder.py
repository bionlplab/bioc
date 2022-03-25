from typing import TextIO, List

from bioc.pubtator.pubtator import PubTatorAnn, PubTatorRel, PubTator


def dumps_ann(ann: PubTatorAnn) -> str:
    return str(ann)


def dumps_rel(rel: PubTatorRel) -> str:
    return str(rel)


def dumps(docs: List[PubTator]) -> str:
    """
    Serialize a list of Pubtator instances to a Pubtator formatted str.

    Args:
        docs: a list of Pubtator documents

    Return:
        a Pubtator formatted str
    """
    return '\n'.join(str(doc) for doc in docs)


def dump(docs: List[PubTator], fp: TextIO):
    """
    Serialize a list of Pubtator instances to file-like object.

    Args:
        docs: a list of Pubtator documents
        fp: a file-like object
    """
    fp.write(dumps(docs))
