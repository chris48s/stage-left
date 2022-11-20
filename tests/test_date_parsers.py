from datetime import date

import pytest

from stage_left import date_parsers

valid_ymd = [
    [["%Y-%m-%d", "2022-01-01"], date(2022, 1, 1)],
    [["%Y/%m/%d", "2022/01/01"], date(2022, 1, 1)],
]

invalid_ymd = [
    ["%Y-%m-%d", "2022-02-31"],  # out of range
    ["%Y/%m/%d", "notadate"],
]


@pytest.mark.parametrize("testcase", valid_ymd)
def test_ymd_valid(testcase):
    input_, expected = testcase
    parsed_date = date_parsers.parse_ymd(*input_)
    assert parsed_date == expected


@pytest.mark.parametrize("testcase", invalid_ymd)
def test_ymd_invalid(testcase):
    with pytest.raises(ValueError):
        date_parsers.parse_ymd(*testcase)


valid_ym = [
    [["%Y-%m", "2022-01"], date(2022, 1, 31)],
    [["%Y/%m", "2022/01"], date(2022, 1, 31)],
    [["%Y/%m", "2022/02"], date(2022, 2, 28)],
    [["%Y/%m", "2020/02"], date(2020, 2, 29)],  # leap year
    [["%Y/%m", "2020/12"], date(2020, 12, 31)],  # December
]

invalid_ym = [
    ["%Y-%m", "2022-13"],  # out of range
    ["%Y/%m", "notadate"],
]


@pytest.mark.parametrize("testcase", valid_ym)
def test_ym_valid(testcase):
    input_, expected = testcase
    parsed_date = date_parsers.parse_ym(*input_)
    assert parsed_date == expected


@pytest.mark.parametrize("testcase", invalid_ym)
def test_ym_invalid(testcase):
    with pytest.raises(ValueError):
        date_parsers.parse_ym(*testcase)


valid_y = [
    ["2022", date(2022, 12, 31)],
    ["2020", date(2020, 12, 31)],  # leap year
]

invalid_y = [
    ["notadate"],
]


@pytest.mark.parametrize("testcase", valid_y)
def test_y_valid(testcase):
    input_, expected = testcase
    parsed_date = date_parsers.parse_y(input_)
    assert parsed_date == expected


@pytest.mark.parametrize("testcase", invalid_y)
def test_y_invalid(testcase):
    with pytest.raises(ValueError):
        date_parsers.parse_y(*testcase)


valid_w = [
    [["%Y-W%W", "2022-W00"], date(2022, 1, 2)],
    [["%Y-W%W", "2022-W01"], date(2022, 1, 9)],
    [["%Y-W%W", "2022-W51"], date(2022, 12, 25)],
    [["%Y-W%W", "2022-W52"], date(2023, 1, 1)],
    [["%Y/W%W", "2022/W00"], date(2022, 1, 2)],
]

invalid_w = [
    ["%Y-W%W", "2022-W54"],  # out of range
    ["%Y/W%W", "notadate"],
]


@pytest.mark.parametrize("testcase", valid_w)
def test_w_valid(testcase):
    input_, expected = testcase
    parsed_date = date_parsers.parse_w(*input_)
    assert parsed_date == expected


@pytest.mark.parametrize("testcase", invalid_w)
def test_w_invalid(testcase):
    with pytest.raises(ValueError):
        date_parsers.parse_w(*testcase)


valid_q = [
    ["2022-Q1", date(2022, 3, 31)],
    ["2022-Q2", date(2022, 6, 30)],
    ["2022-Q3", date(2022, 9, 30)],
    ["2022-Q4", date(2022, 12, 31)],
    ["2022/Q1", date(2022, 3, 31)],
    ["2022/Q2", date(2022, 6, 30)],
    ["2022/Q3", date(2022, 9, 30)],
    ["2022/Q4", date(2022, 12, 31)],
]

invalid_q = [
    ["2022-Q5"],  # out of range
    ["notadate"],
]


@pytest.mark.parametrize("testcase", valid_q)
def test_q_valid(testcase):
    input_, expected = testcase
    parsed_date = date_parsers.parse_q(input_)
    assert parsed_date == expected


@pytest.mark.parametrize("testcase", invalid_q)
def test_q_invalid(testcase):
    with pytest.raises(ValueError):
        date_parsers.parse_q(*testcase)
