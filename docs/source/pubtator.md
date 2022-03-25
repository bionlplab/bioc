# PubTator

pubtator's interfaces for processing PubTator file are grouped in the `pubtator` package.

## Encoding the PubTator object

Encoding the PubTator document object `doc`:

```python
from bioc import pubtator
# Serialize ``doc`` to a PubTator formatted ``str``.
pubtator.dumps([doc])
# Serialize ``collection`` as a BioC formatted stream to ``fp``.
with open(filename, 'w') as fp:
    pubtator.dump([doc], fp)
```

## Decoding the PubTator file

```python
from bioc import pubtator
# Deserialize ``s`` to a PubTator object.
docs = pubtator.loads(s)
# Deserialize ``fp`` to a PubTator object.
with open(filename, 'r') as fp:
    docs = pubtator.load(fp)
```

Incrementally decoding the PubTator file:

```python
from bioc import pubtator
# read from a file
with open(filename) as fp:
    for doc in pubtator.iterparse(fp):
        # process document
        ...
```

## Converting from PubTator to a BioC

```python
from bioc import pubtator
from bioc.tools.pubtator2bioc import pubtator2bioc
docs = pubtator.loads(text)

# Convert a list of PubTator docs to a BioC collection object.
collection = pubtator2bioc(docs)
```