import re
import sys
import unicodedata

_TAG_START = r"\#"
_TAG_KEY = r"([\w\d_-]+)"


_VALUE_ONLY_END = r"(?=[^\w\d_-]|$)"
VALUE_ONLY_TAG_PATTERN = re.compile(_TAG_START + _TAG_KEY + _VALUE_ONLY_END, re.U)


DOUBLE_QUOTED_KEY_VALUE_TAG_PATTERN = re.compile(
    _TAG_START + _TAG_KEY + r"=(\".*?\")", re.U
)


SINGLE_QUOTED_KEY_VALUE_TAG_PATTERN = re.compile(
    _TAG_START + _TAG_KEY + r"=('.*?')", re.U
)


_UNICODE_PUNCTUATION = [
    chr(i)
    for i in range(sys.maxunicode)
    if unicodedata.category(chr(i)).startswith("P")
]
_TAG_UNICODE_PUNCTUATION = "".join([c for c in _UNICODE_PUNCTUATION])
_UNQUOTED_KEY_VALUE_END = r"(?=[ " + _TAG_UNICODE_PUNCTUATION + r"]|$)"
UNQUOTED_KEY_VALUE_TAG_PATTERN = re.compile(
    _TAG_START + _TAG_KEY + r"=([\w\d_-]*)" + _UNQUOTED_KEY_VALUE_END, re.U
)
