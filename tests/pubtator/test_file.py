from pathlib import Path

from bioc import pubtator


def test_iterparse():
    filepath = Path(__file__).parent / 'tmVar.Normalization.txt'
    print(filepath)
    with open(filepath) as fp:
        docs = [doc for doc in pubtator.iterparse(fp)]

    assert len(docs) == 158
