import pytest

from stage_left.parser import parse_text
from stage_left.types import Group, Item, ParseError, State

valid_groups = """
[ ] Item 1 of group
[ ] Item 2 of group

[ ] Item of another group

Todos
[ ] Item 1
[ ] Item 2

Group 1
[ ] Item
         
Group 2
[ ] Item

Empty Group
"""  # noqa:W293

leading_whitespace1 = """ Todos
[ ] Do this
"""

leading_whitespace2 = """    Todos
[ ] Do this
"""

opening_square_bracket = """[Todos]
[ ] Do this
"""

no_blank_line = """[ ] Do this
Todos
[ ] Do this
"""

invalid_groups = [
    leading_whitespace1,
    leading_whitespace2,
    opening_square_bracket,
    no_blank_line,
]


def test_groups_valid():
    expected = [
        Group(
            items=[
                Item(
                    state=State.OPEN,
                    description="Item 1 of group",
                    tags=[],
                    priority=0,
                    due_date=None,
                ),
                Item(
                    State.OPEN,
                    description="Item 2 of group",
                    tags=[],
                    priority=0,
                    due_date=None,
                ),
            ],
            title="",
        ),
        Group(
            items=[
                Item(
                    State.OPEN,
                    description="Item of another group",
                    tags=[],
                    priority=0,
                    due_date=None,
                )
            ],
            title="",
        ),
        Group(
            items=[
                Item(
                    State.OPEN,
                    description="Item 1",
                    tags=[],
                    priority=0,
                    due_date=None,
                ),
                Item(
                    State.OPEN,
                    description="Item 2",
                    tags=[],
                    priority=0,
                    due_date=None,
                ),
            ],
            title="Todos",
        ),
        Group(
            items=[
                Item(
                    State.OPEN,
                    description="Item",
                    tags=[],
                    priority=0,
                    due_date=None,
                )
            ],
            title="Group 1",
        ),
        Group(
            items=[
                Item(
                    State.OPEN,
                    description="Item",
                    tags=[],
                    priority=0,
                    due_date=None,
                )
            ],
            title="Group 2",
        ),
        Group(items=[], title="Empty Group"),
    ]
    assert parse_text(valid_groups) == expected


@pytest.mark.parametrize("group", invalid_groups)
def test_groups_invalid(group):
    with pytest.raises(ParseError):
        parse_text(group)
