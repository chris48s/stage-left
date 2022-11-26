import re

from stage_left.date_patterns import DUE_DATE_PATTERNS
from stage_left.tag_patterns import (
    DOUBLE_QUOTED_KEY_VALUE_TAG_PATTERN,
    SINGLE_QUOTED_KEY_VALUE_TAG_PATTERN,
    UNQUOTED_KEY_VALUE_TAG_PATTERN,
    VALUE_ONLY_TAG_PATTERN,
)


def strip_tags(text):
    return re.sub(
        VALUE_ONLY_TAG_PATTERN,
        "",
        re.sub(
            UNQUOTED_KEY_VALUE_TAG_PATTERN,
            "",
            re.sub(
                DOUBLE_QUOTED_KEY_VALUE_TAG_PATTERN,
                "",
                re.sub(SINGLE_QUOTED_KEY_VALUE_TAG_PATTERN, "", text),
            ),
        ),
    )


def strip_due_date(text):
    for regex in DUE_DATE_PATTERNS.keys():
        matches = re.search(regex, text)
        if matches:
            return re.sub(regex, "", text)
