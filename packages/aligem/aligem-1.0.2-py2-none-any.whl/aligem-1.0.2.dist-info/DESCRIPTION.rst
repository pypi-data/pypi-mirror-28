# AliGEM

AliGEM (ALICE Grid Environment Manger) is a simple tool for handling [CERN Grid](http://wlcg.web.cern.ch) jobs related elemental operation used by collaboration of [ALICE](http://aliceinfo.cern.ch/Public/Welcome.html) experiment at the LHC.

## Motivation
The original motivation behind this tool is to provide a unified way to execute simple operations which was (commonly) used as a collection of individual bash scripts with all its pros and cons.

## Installation
AliGEM package is available on [PyPI](https://pypi.python.org/pypi/aligem) and thus it can be installed via `pip` simply by

```
pip install aligem
```

## Usage
Once installed, one can invoke use aligem tool directly from command-line. Brief overview of available operations together with their description can be invoked by `aligem -h`.

```
aligem [-h] [-v] [-d] [--version] {jobs,token} ...

operations
  {jobs,token}
    jobs         grid jobs operations
    token        token (not implemented yet)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  produce verbose output
  -d, --debug    debugging mode (additional printout)
  --version      print current version
```

A detailed description is provided bellow.

### AliEn token operations
`aligem token -h`


