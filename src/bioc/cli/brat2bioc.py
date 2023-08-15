"""
Usage:
    brat2bioc -d DIR -o FILE

Options:
    -d DIR      Brat input directory
    -o FILE     BioC output file
"""
import bioc
from bioc.tools.brat2bioc import brat2bioc
from bioc import brat


from docopt import docopt


def main():
    args = docopt(__doc__)
    bratdocs = brat.listdir(args['-d'])
    c = brat2bioc(bratdocs)
    with open(args['-o'], 'w') as fp:
        bioc.dump(c, fp)


if __name__ == '__main__':
    main()