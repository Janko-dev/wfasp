
# Wave Function Collapse using ASP

This repo contains an Answer Set Programming (ASP) based implementation of the Wave Function Collapse (WFC) algorithm. The ASP grounder and solver `clingo` is used, which enables multi-shot solving capabilities. This feature allows for logic programs to interact with the external world via a (Python) API. The implementation consists of a combinatorial logic encoding that utilises choice constructs and integrity constraints, and an incremental-solving encoding, which solves small increments of the problem in an iterative procedure.

https://github.com/Janko-dev/wfcasp/assets/46781046/157e6262-f343-41ac-a142-1ce6ddaf7f20

## Quick start

```
$ cd encoding_incremental/
$ python control.py rules/simple_rules.lp simple_tiles/ -dim 8 8
```

### Usage
```
usage: control.py [-h] [-n [N]] [-dim DIM DIM] rules [tileset_folder]

Wave Function Collapse

positional arguments:
  rules           path to rules logic program
  tileset_folder  path to folder with .png tileset.

optional arguments:
  -h, --help      show this help message and exit
  -n [N]          number of patterns in NxN square to consider
  -dim DIM DIM    width and height of output image
```

