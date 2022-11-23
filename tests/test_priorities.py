import pytest

from stage_left.parser import classify_lines, parse_item

not_important = """[ ] This is also
    !!! not important"""

valid_priorities = [
    ["[ ] ! This is important", 1],
    ["[ ] !!! This is very important", 3],
    ["[ ] !!!!!!!!!! This super important", 10],
    ["[ ] ..! This is important", 1],
    ["[ ] !!. This is more important", 2],
    ["[ ] ... This is not important", 0],
    ["[ ] !   Do something", 1],
    ["[ ] .   Do something", 0],
    ["[ ] !This has regular priority", 0],
    ["[ ] .The dot is not priority", 0],
    [not_important, 0],
    ["[ ] ! !!! This is important!", 1],
    ["[ ] !! ! ! This ! is also important", 2],
    ["[ ] !. ... This . is also important", 1],
    ["[ ] . ! This is not important", 0],
]

invalid_priorities = [
    "[ ]    ! Do something",
    "[ ]    . Do something",
    "[ ] .!. Invalid",
    "[ ] !.! Invalid",
    "[ ] !.!. Invalid",
]


@pytest.mark.parametrize("item", valid_priorities)
def test_priorities_valid(item):
    input_, expected = item
    parsed_item = parse_item(classify_lines([input_]))
    assert parsed_item.priority == expected


@pytest.mark.parametrize("item", invalid_priorities)
def test_priorities_invalid(item):
    parsed_item = parse_item(classify_lines([item]))
    assert parsed_item.priority == 0
