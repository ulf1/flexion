[![PyPI version](https://badge.fury.io/py/flexion.svg)](https://badge.fury.io/py/flexion)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4284804.svg)](https://doi.org/10.5281/zenodo.4284804)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/ulf/flexion/master?urlpath=lab)
[![Gitpod - Code Now](https://img.shields.io/badge/Gitpod-code%20now-blue.svg?longCache=true)](https://gitpod.io#https://github.com/ulf/flexion)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/ulf/flexion.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ulf/flexion/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ulf/flexion.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ulf/flexion/context:python)

# flexion
Applying declination and conjugation rules to lemmata.


## Usage



## Appendix

### Installation in another project
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

### Install a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
pip install -r requirements-demo.txt --no-cache-dir
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
