"""
Usage:
    split [options] INPUT PREFIX

Options:
    -a N --suffix-length=N          generate suffixes of length N [default: 2]
    --additional-suffix=SUFFIX      append an additional SUFFIX to file names
    [default: .xml]
    -d NUMBER --documents=NUMBER    put NUMBER docs per output file
    [default: 100]
"""
from docopt import docopt

from bioc.tools.split import split_file


def main():
    args = docopt(__doc__)
    print(args)
    split_file(args['INPUT'],
               prefix=args['PREFIX'],
               num_doc=int(args['--documents']),
               suffix_length=int(args['--suffix-length']),
               additional_suffix=args['--additional-suffix'])


if __name__ == '__main__':
    main()