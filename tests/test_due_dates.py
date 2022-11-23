from datetime import date

import pytest

from stage_left import ParseError
from stage_left.parser import classify_lines, parse_item

valid_date_on_continuation_line = """[ ] Do something until ...
    -> 2022-01-31"""

valid_due_dates = [
    ["[ ] -> 2022-01-31", date(2022, 1, 31)],
    ["[ ] Do this -> 2022-01-31", date(2022, 1, 31)],
    ["[ ] -> 2022-01-31 (something)", date(2022, 1, 31)],
    [valid_date_on_continuation_line, date(2022, 1, 31)],
    ["[ ] -> 2022-01-31", date(2022, 1, 31)],
    ["[ ] -> 2022-01", date(2022, 1, 31)],
    ["[ ] -> 2022", date(2022, 12, 31)],
    ["[ ] -> 2022-W01", date(2022, 1, 9)],
    ["[ ] -> 2022-Q1", date(2022, 3, 31)],
    ["[ ] -> 2022/01/31", date(2022, 1, 31)],
    ["[ ] -> 2022/W01", date(2022, 1, 9)],
    ["[ ] -> 2022-01-31 -> 2022-02-01", date(2022, 1, 31)],
    ["[ ] Do this soon -> 2022-01-31!!!", date(2022, 1, 31)],
    ["[ ] Do this (-> 2022-01-31)", date(2022, 1, 31)],
]

invalid_date_on_continuation_line = """[ ] Do until ->
    2022-01-31"""

invalid_due_dates = [
    "[ ] -> 2022-01/31",
    "[ ] ---> 2022-01-31",
    "[ ] Due-> 2022-01-31",
    "[ ] -> 2022-01-31very urgent",
    "[ ] -> 2022-01-31T10:00",
    "[ ] -> 2022-01-31-0",
    "[ ] -> 2022/01/31/0",
    "[ ] ->2022-01-31",
    "[ ] → 2022-01-31",
    "[ ] ->   2022-01-31",
    "[ ] >2022-01-31",
    invalid_date_on_continuation_line,
]


@pytest.mark.parametrize("item", valid_due_dates)
def test_due_dates_valid(item):
    input_, expected = item
    parsed_item = parse_item(classify_lines([input_]))
    assert parsed_item.due_date == expected


@pytest.mark.parametrize("item", invalid_due_dates)
def test_priorities_invalid(item):
    parsed_item = parse_item(classify_lines([item]))
    assert parsed_item.due_date is None


def test_priorities_exception():
    with pytest.raises(ParseError):
        parse_item(classify_lines(["[ ] Not a real date -> 2022-02-31"]))
