"""
Usage:
    split [options] INPUT PREFIX

Options:

    -a N --suffix-length=N          generate suffixes of length N [default: 2]
    --additional-suffix=SUFFIX      append an additional SUFFIX to file names [default: .xml]
    -d NUMBER --documents=NUMBER    put NUMBER docs per output file [default: 100]
"""
from docopt import docopt
import tqdm
from src import bioc


def split(source, *, prefix: str, num_doc: int, additional_suffix: str = '.xml',
          suffix_length: int = 2):
    path_format = prefix + '{:0' + str(suffix_length) + 'x}' + additional_suffix

    with open(source, encoding='utf8') as fp:
        collection = bioc.load(fp)

    newc = bioc.BioCCollection()
    newc.infons = collection.infons
    newc.source = collection.source
    newc.version = collection.version
    newc.source = collection.source
    newc.standalone = collection.standalone

    i = 0
    for doc in tqdm.tqdm(collection.documents):
        newc.add_document(doc)
        if len(newc.documents) == num_doc:
            dst = path_format.format(i)
            with open(dst, 'w', encoding='utf8') as fp:
                bioc.dump(newc, fp)
            del newc.documents[:]
            i += 1
    if newc.documents:
        dst = path_format.format(i)
        with open(dst, 'w', encoding='utf8') as fp:
            bioc.dump(newc, fp)


if __name__ == '__main__':
    args = docopt(__doc__)
    print(args)
    split(args['INPUT'],
          prefix=args['PREFIX'],
          num_doc=int(args['--documents']),
          suffix_length=int(args['--suffix-length']),
          additional_suffix=args['--additional-suffix'])
