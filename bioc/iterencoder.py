import lxml.etree as etree
from .bioc import BioCCollection
from .encoder import encode_infon, encode_document


class BioCEncoderIter(object):
    def __writer__(self):
        with etree.xmlfile(self.file, encoding=self.collection.encoding, close=True) as xf:
            xf.write_declaration(standalone=self.collection.standalone)
            with xf.element('collection'):
                try:
                    while True:
                        el = (yield)
                        xf.write(el)
                        xf.write('\n')
                        xf.flush()
                except GeneratorExit:
                    pass

    def __init__(self, name, collection=None):
        """
        Returns an object of the BioCEncoderIter which can write an BioC file incrementally at document level.
        :param name: file name to be decoded
        """

        self.file = name
        if not collection:
            collection = BioCCollection()
        self.collection = collection
        self.w = self.__writer__()
        next(self.w)   # start writing (run up to 'yield')

        elem = etree.Element('source')
        elem.text = self.collection.source
        self.w.send(elem)

        elem = etree.Element('date')
        elem.text = self.collection.date
        self.w.send(elem)

        elem = etree.Element('key')
        elem.text = self.collection.key
        self.w.send(elem)

        for k, v in self.collection.infons.items():
            elem = encode_infon(k, v)
            self.w.send(elem)

    def __write_infons(self, infons):
        for k, v in infons.items():
            elem = etree.Element('infon', {'key': str(k)})
            elem.text = str(v)
            self.w.send(elem)

    def close(self):
        self.w.close()

    def writedocument(self, document):
        tree = encode_document(document)
        self.w.send(tree)

