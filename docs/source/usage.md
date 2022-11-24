# Usage Examples

## Parse checklist from file

```py
from stage_left import parse_file, ParseError

with open("/path/to/checklist.xit") as fp:
    try:
        checklist = parse_file(fp)
    except ParseError:
        raise
```

## Parse checklist from string

```py
from stage_left import parse_text, ParseError

text = """
[ ] Open
[x] Done
"""

try:
    checklist = parse_text(text)
except ParseError:
    raise
```
