import math
import string
import tempfile

from docopt import docopt

import bioc
from bioc.tools import split
import random


def get_random_str():
    return ''.join(random.choices(string.ascii_letters + string.digits + ' ',
                                  k=random.randint(10, 500)))


def get_collection(total_doc):
    c = bioc.BioCCollection()
    c.source = 'source'
    for i in range(total_doc):
        text = get_random_str()
        doc = bioc.BioCDocument.of_text(text)
        c.add_document(doc)
    return c


def test_itersplit():
    total_doc = 230
    n = 7
    c = get_collection(total_doc)
    cs = list(split.itersplit(c, n))
    for i in range(int(total_doc / n)):
        subc = cs[i]
        assert len(subc.documents) == n

    last_n = int(math.ceil(total_doc / n))
    if last_n > int(total_doc / n):
        subc = cs[last_n-1]
        assert len(subc.documents) == total_doc % n


def test_split_file(tmp_path):
    total_doc = 230
    n = 7
    c = get_collection(total_doc)

    source = tmp_path / 'foo.xml'
    with open(source, 'w') as fp:
        bioc.dump(c, fp)

    split.split_file(source, prefix=str(tmp_path), num_doc=n)
    for i in range(int(total_doc/n)):
        source = str(tmp_path) + '{:02x}.xml'.format(i)
        with open(source) as fp:
            subc = bioc.load(fp)
            assert len(subc.documents) == n

    last_n = int(math.ceil(total_doc/n))
    if last_n > int(total_doc/n):
        source = str(tmp_path) + '{:02x}.xml'.format(last_n-1)
        with open(source) as fp:
            subc = bioc.load(fp)
            assert len(subc.documents) == total_doc % n


def test_cli():
    cmd = 'split -a 5 --additional-suffix=.txt -d 150 INPUT PREFIX'
    argv = docopt(split.__doc__, argv=cmd.split()[1:])
    assert argv['--suffix-length'] == '5'
    assert argv['--additional-suffix'] == '.txt'
    assert argv['INPUT'] == 'INPUT'
    assert argv['PREFIX'] == 'PREFIX'
