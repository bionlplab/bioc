# Brat

[brat standoff format](https://brat.nlplab.org/standoff.html) is created by the brat annotation tool to store
annotations on disk in a standoff format. annotations are stored separately from the annotated document text, which is
never modified by the tool.

pubtator's interfaces for processing PubTator file are grouped in the `pubtator` package.

## Encoding the Brat object

Encoding the Brat document object `doc`:

```python
from bioc import brat
# Serialize ``doc`` to a brat formatted ``str``.
brat.dumps_ann(doc)
# Serialize ``doc`` as a brat formatted stream to ``text_fp`` and ``ann_fp``.
with open(annpath, 'w') as ann_fp, open(txtpath, 'w') as text_fp:
    brat.dump(doc, text_fp, ann_fp)
```

## Decoding the Brat file

```python
from bioc import brat
# Deserialize ``s`` to a PubTator object.
doc = brat.loads(text, ann)
# Deserialize ``fp`` to a PubTator object.
with open(annpath) as ann_fp, open(txtpath) as text_fp:
    doc = brat.load(text_fp, ann_fp)
```

Decoding the files in a folder:

```python
from bioc import brat
# read from a file
for doc in brat.iterloaddir(dirname):
    # process document
    ...
```

## Converting from Brat to a BioC

```python
from bioc import brat
from bioc.tools.brat2bioc import brat2bioc
docs = brat.loaddir(dirname)

# Convert a list of Brat docs to a BioC collection object.
collection = brat2bioc(docs)
```
