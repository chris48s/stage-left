import sys
import unicodedata

_UNICODE_PUNCTUATION = [
    chr(i)
    for i in range(sys.maxunicode)
    if unicodedata.category(chr(i)).startswith("P")
]
_DATE_UNICODE_PUNCTUATION = "".join(
    [c for c in _UNICODE_PUNCTUATION if c not in ["-", "/"]]
)

_DATE_FORMATS = [
    # TODO:
    # these regular expressions are quite crude
    # e.g: they will accept 2022-02-31 as a "date"
    # the next step to making this better
    # is to try and parse the matches into a date object
    r"(\d{4}-\d{2}-\d{2})",  # yyyy-mm-dd
    r"(\d{4}/\d{2}/\d{2})",  # yyyy/mm/dd
    r"(\d{4}[-/]\d{2})",  # yyyy-mm or yyyy/mm
    r"(\d{4}[-/]W\d{2})",  # yyyy-Www or yyyy/Www
    r"(\d{4}[-/]Q\d{1})",  # yyyy-Qq or yyyy/Qq
    r"(\d{4})",  # yyyy
]

_DUE_DATE_START = r"([ " + _DATE_UNICODE_PUNCTUATION + r"]|^)-> "
_DUE_DATE_END = r"(?=[ " + _DATE_UNICODE_PUNCTUATION + r"]|$)"

DUE_DATE_PATTERNS = [_DUE_DATE_START + DF + _DUE_DATE_END for DF in _DATE_FORMATS]
