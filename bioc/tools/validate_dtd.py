"""
Usage:
    validate DTD XML
"""
from docopt import docopt
from lxml import etree


class DTDValidator:
    def __init__(self, dtd_path):
        self.dtd = etree.DTD(dtd_path)

    def validate(self, xml_path):
        xml_doc = etree.parse(xml_path)
        result = self.dtd.validate(xml_doc)
        return result


if __name__ == '__main__':
    args = docopt(__doc__)
    validator = DTDValidator(args['DTD'])
    result = validator.validate(args['XML'])
    if result:
        print('Valid!')
    else:
        print('Not valid!')
        log = validator.dtd.error_log
        print(log)
