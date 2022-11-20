# stage-left

[![Run tests](https://github.com/chris48s/stage-left/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/chris48s/stage-left/actions/workflows/test.yml)
<!-- TODO: codecov badge -->
[![PyPI Version](https://img.shields.io/pypi/v/stage-left.svg)](https://pypi.org/project/stage-left/)
![License](https://img.shields.io/pypi/l/stage-left.svg)
![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fstage-left%2Fjson)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

[[x]it!](https://xit.jotaen.net/) is a plain-text file format for todos and check lists. Stage-left parses [x]it! documents into rich python objects.

## Installation

```
pip install stage-left
```

## Usage

### Parse checklist from file

```py
from stage_left import parse_file, ParseError

with open("/path/to/checklist.xit") as fp:
    try:
        checklist = parse_file(fp)
        print(checklist)
    except ParseError:
        raise
```

### Parse checklist from string

```py
from stage_left import parse_text, ParseError

text = """
[ ] Open
[x] Done
"""

try:
    checklist = parse_text(text)
    print(checklist)
except ParseError:
    raise
```

## Implementation notes

Due dates specified using the numbered week syntax e.g: `2022-W01` are parsed assuming Monday is the first day of the week. All days in a new year preceding the first Monday are considered to be in week 0 (`W00`).
