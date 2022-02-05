"""
Usage:
    validate XSD XML
"""
from docopt import docopt
from lxml import etree


class XSDValidator:
    def __init__(self, xsd_path):
        xmlschema_doc = etree.parse(xsd_path)
        self.xmlschema = etree.XMLSchema(xmlschema_doc)

    def validate(self, xml_path):
        xml_doc = etree.parse(xml_path)
        result = self.xmlschema.validate(xml_doc)
        return result


if __name__ == '__main__':
    args = docopt(__doc__)
    validator = XSDValidator(args['XSD'])
    result = validator.validate(args['XML'])
    if result:
        print('Valid!')
    else:
        print('Not valid!')
        log = validator.xmlschema.error_log
        print(log)
