import sys
import unicodedata
from functools import partial

from stage_left import date_parsers

_DATE_PARSERS = {
    r"(\d{4}-\d{2}-\d{2})": partial(date_parsers.parse_ymd, "%Y-%m-%d"),
    r"(\d{4}/\d{2}/\d{2})": partial(date_parsers.parse_ymd, "%Y/%m/%d"),
    r"(\d{4}-\d{2})": partial(date_parsers.parse_ym, "%Y-%m"),
    r"(\d{4}/\d{2})": partial(date_parsers.parse_ym, "%Y/%m"),
    r"(\d{4}-W\d{2})": partial(date_parsers.parse_w, "%Y-W%W"),
    r"(\d{4}/W\d{2})": partial(date_parsers.parse_w, "%Y/W%W"),
    r"(\d{4}-Q\d{1})": date_parsers.parse_q,
    r"(\d{4}/Q\d{1})": date_parsers.parse_q,
    r"(\d{4})": date_parsers.parse_y,
}


_UNICODE_PUNCTUATION = [
    chr(i)
    for i in range(sys.maxunicode)
    if unicodedata.category(chr(i)).startswith("P")
]
_DATE_UNICODE_PUNCTUATION = "".join(
    [c for c in _UNICODE_PUNCTUATION if c not in ["-", "/"]]
)

_DUE_DATE_START = r"([ " + _DATE_UNICODE_PUNCTUATION + r"]|^)-> "
_DUE_DATE_END = r"(?=[ " + _DATE_UNICODE_PUNCTUATION + r"]|$)"

DUE_DATE_PATTERNS = {
    _DUE_DATE_START + regex + _DUE_DATE_END: parser
    for regex, parser in _DATE_PARSERS.items()
}
