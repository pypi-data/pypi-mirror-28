# pyinverted
[![docs](https://readthedocs.org/projects/pyinverted/badge/?version=latest)](http://pyinverted.readthedocs.io/en/latest/?badge=latest)

*pyinverted* implements a class for inverted files creation and managing.

First, the class creates/opens a file `.dict`. This file has the inverted file
dictionary saved with Python's [*pickle*](https://docs.python.org/3.2/library/pickle.html).
The dictionary is structed as `<some key>: <list's index in .inv>`.

Second, the class also creates/opens another file: `.inv`. This file has a list of `values` for
each `key`.

This implementation can be used as a searching tool for records in a file.

## Installation
```bash
$ pip3 install pyinverted
```

## Example
```python
from pyinverted import Inverted

# Open two files: names.dict, names.inv
inv = Inverted('names')

# Return all values associated with PEANUT
peanut = inv.get('PEANUT')
```

## Docs and stuff
You can find docs, api and examples in [here](http://pyinverted.readthedocs.io/en/latest/).
