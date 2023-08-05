# pystrct
A binary file's manager in Python 3.

*pystrct* creates and manages a binary file using Python's *Struct*.
You can access any file's record by index as in array.

## Installation
```shell
$ pip3 install pystrct
```

## Example
```python
from pystrct import StructFile

file = StructFile('numbers.bin', 'i')  # open a file named 'numbers.bin' structed as integers ('i')

n1 = file.get(4)                       # get the 4th number on file
n2 = file.next()                       # get the 5th number
```

## Docs and stuff
