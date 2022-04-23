[![PyPI version](https://badge.fury.io/py/flexion.svg)](https://badge.fury.io/py/flexion)
[![PyPi downloads](https://img.shields.io/pypi/dm/flexion)](https://img.shields.io/pypi/dm/flexion)
[![DOI](https://zenodo.org/badge/441439427.svg)](https://zenodo.org/badge/latestdoi/441439427)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/ulf/flexion.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ulf/flexion/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ulf/flexion.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ulf/flexion/context:python)


# flexion
Applying declination and conjugation rules to lemmata.

## 🤙 Call for Collaborators
I'm looking for a collaborator with knowledge about (or interest in) German linguistics; in particular syntax & morphology.
Poeple with limited programming experience are welcome.
Drop me a message: `hamster` [ät] "bbaw" (dot) 'de'.

## ⚠️ Warning
Software is **not** production ready and requires more unit testing.

**Known Problems:**
The software should work for `VERB` and `ADJ`.
It will fail for the genus of relative pronouns and coreference resolution if the genus of replaced `NOUN` changes.

## ✔️ Bender Rule
The software was developed for processing German-language texts (lang: de).

## ⚙️ Installation in another project
The `flexion` [git repo](http://github.com/ulf/flexion) is available as [PyPi package](https://pypi.org/project/flexion)

```sh
pip install flexion
```

Download a Transducer model
```
python scripts/download_transducer.py --model=smor
```

Download demo data for unit tests
```
mkdir tmp
wget -O tmp/de_hdt-ud-dev.conllu https://raw.githubusercontent.com/UniversalDependencies/UD_German-HDT/master/de_hdt-ud-dev.conllu 
```

## 🛠️ Usage
The `flexion.replace` function expects a sentence formated as [conllu](https://pypi.org/project/conllu/) dictionary.

```py
import flexion
import io
import conllu

# read CoNLL-U data
iowrapper = io.open("tmp/de_hdt-ud-dev.conllu", "r", encoding="utf-8")
dat = [s for s in conllu.parse_incr(iowrapper)]

# select a sentence examples
print(dat[5].metadata.get('text'))
# '" Diesen Gerüchten liegt eine unseriöse Recherche zugrunde .'

# Generate augmentations
lemma = "Gerücht"
substitute = "Spekulation"
augmentations = flexion.replace(lemma, substitute, dat[5])
print(augmentations)
# ['" Diesen Spekulationen liegt eine unseriöse Recherche zugrunde.']
```

You can use packages like SpaCy, TranKit or Stanza to parse sentences and transform them to Python dictionary with [CoNLL-U fields](https://universaldependencies.org/format.html) as keys.
See [this notebook](https://github.com/ulf1/flexion/blob/main/demo/Augment%20Sentences%20with%20flexion%20and%20spacy.ipynb) for examples.


## Appendix

### Install a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir

# jupyter notebooks
pip install -r requirements-demo.txt --no-cache-dir
python -m spacy download de_core_news_lg
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Python commands

* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `PYTHONPATH=. pytest`

Publish

```sh
pandoc README.md --from markdown --to rst -s -o README.rst
python setup.py sdist 
twine upload -r pypi dist/*
```

### Clean up 

```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


### Support
Please [open an issue](https://github.com/ulf/flexion/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf/flexion/compare/).
