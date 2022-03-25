# bioc - BioC data structures and encoder/decoder for Python

[![Build
status](https://github.com/bionlplab/bioc/actions/workflows/pytest.yml/badge.svg)](https://github.com/bionlplab/bioc/)
[![Latest version on
PyPI](https://img.shields.io/pypi/v/bioc.svg)](https://pypi.python.org/pypi/bioc)
[![Downloads](https://img.shields.io/pypi/dm/bioc.svg)](https://pypi.python.org/pypi/bioc)
[![License](https://img.shields.io/pypi/l/bioc.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/bionlplab/bioc/branch/master/graph/badge.svg?token=3kEUctqxTx)](https://codecov.io/gh/bionlplab/bioc)

[BioC XML / JSON format](http://bioc.sourceforge.net/) can be used to
share text documents and annotations.

`bioc` exposes an API familiar to users of the standard library
`marshal` and `pickle` modules.

Development of `bioc` happens on GitHub:
<https://github.com/bionlplab/bioc>

## Getting started

Installing `bioc`

```shell
$ pip install bioc
```

Encoding the BioC collection object `collection`:

```python
import bioc
# Serialize ``collection`` as a BioC formatted stream to ``fp``.
with open(filename, 'w') as fp
    bioc.dump(collection, fp)
```

Decoding the BioC XML file:

```python
import bioc
# Deserialize ``fp`` to a BioC collection object.
with open(filename, 'r') as fp:
    collection = bioc.load(fp)
```

## Documentation

You will find complete documentation at our [Read the Docs
site](https://bioc.readthedocs.io/en/latest/index.html).

## Contributing

You can find information about contributing to RadText at our [Contribution
page](https://bioc.readthedocs.io/en/latest/contribute.html).

## Webpage

The official BioC webpage is available with all up-to-date instructions,
code, and corpora in the BioC format, and other research on, based on
and related to BioC.

  - <http://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/BioC/>
  - <http://bioc.sourceforge.net/>

## Reference

If you use bioc in your research, please cite the following paper:

  - Comeau DC, Doğan RI, Ciccarese P, Cohen KB, Krallinger M, Leitner F, Lu Z, Peng Y, Rinaldi F, Torii M, 
    Valencia V, Verspoor K, Wiegers TC, Wu CH, Wilbur WJ. BioC: a minimalist approach to interoperability 
    for biomedical text processing. Database (Oxford). 2013;2013:bat064. doi: 10.1093/database/bat064. 
    Print 2013. PMID: 24048470; PMCID: PMC3889917
    
## Acknowledgment

This work is supported by the National Library of Medicine under Award No.
4R00LM013001.
    
## License

Copyright BioNLP Lab at Weill Cornell Medicine, 2022.

Distributed under the terms of the [MIT](https://github.com/bionlplab/bioc/blob/master/LICENSE) license, 
bioc is free and open source software.
