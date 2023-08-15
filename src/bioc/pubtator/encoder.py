from typing import TextIO, List

from bioc.pubtator.datastructure import PubTatorAnn, PubTatorRel, PubTator


def dumps_ann(ann: PubTatorAnn) -> str:
    return str(ann)


def dumps_rel(rel: PubTatorRel) -> str:
    return str(rel)


def dumps(docs: List[PubTator]) -> str:
    """
    Serialize a list of Pubtator instances to a Pubtator formatted str.

    :param docs: a list of Pubtator documents
    """
    return '\n'.join(str(doc) for doc in docs)


def dump(docs: List[PubTator], fp: TextIO):
    """
    Serialize a list of Pubtator instances to file-like object.

    :param docs: a list of Pubtator documents
    :param fp: a file-like object
    """
    fp.write(dumps(docs))
