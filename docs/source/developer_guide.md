# Developer guide

## Development Installation

These are development setup. If you are a contributor to bioc, it might a be
a good idea to follow these guidelines as well.

## Compile from source

bioc is actively developed on [GitHub repository](https://github.com/bionlplab/bioc).
The other way to install bioc is to clone its GitHub repository.

```shell
# Checkout repository
$ git clone https://github.com/bionlplab/bioc.git
$ cd bioc

# Set up Python environment
$ python -m venv venv
$ source venv/bin/activate

# Install dependencies
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt
```

## Test the code

```shell
$ pytest --cov html tests
```

## Create this documentation

We use Sphinx and MyST to generate documentation.

```shell
$ pip install sphinx sphinx_rtd_theme myst-parser
$ cd docs
$ make html
```

## Publish BioC to PyPI and TestPyPI

First, you need a PyPI user account. You can create an account using the
form on the PyPI/TestPyPI website.

Now you’ll create a PyPI/TestPyPI API token so you will be able to
securely upload your project.

Go to <https://pypi.org/manage/account/#api-tokens> and create a new API
token; don’t limit its scope to a particular project, since you are
creating a new project.

```shell
$ pip install build twine
$ python -m build
```

Using local package with pip

```shell
$ pip install --force-reinstall dist/PACKAGE.whl
```

Using TestPyPI with pip

```shell
$ twine upload --repository testpypi dist/*
$ pip install --index-url https://test.pypi.org/simple/ bioc
```
