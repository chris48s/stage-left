from datetime import date
from pathlib import Path

from stage_left.parser import parse_file, parse_text
from stage_left.types import Group, Item, State, Tag


def test_integration():
    expected = [
        Group(
            items=[
                Item(
                    state=State.OPEN,
                    description="Item 1",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    State.OPEN,
                    description="Item 2",
                    tags=set(),
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
                    description="This #item #has=tags",
                    tags={Tag(value="item"), Tag(key="has", value="tags")},
                    priority=0,
                    due_date=None,
                ),
                Item(
                    State.OPEN,
                    description="Do this soon -> 2022-01-31",
                    tags=set(),
                    priority=0,
                    due_date=date(2022, 1, 31),
                ),
                Item(
                    State.OPEN,
                    description="!! This is important",
                    tags=set(),
                    priority=2,
                    due_date=None,
                ),
                Item(
                    State.OPEN,
                    description="! All #the=things -> 2022-12",
                    tags={Tag(key="the", value="things")},
                    priority=1,
                    due_date=date(2022, 12, 31),
                ),
            ],
            title="Group",
        ),
    ]
    with open(Path(".") / "tests" / "fixtures" / "example.xit") as fp:
        assert parse_file(fp) == expected

        fp.seek(0)
        document = fp.read()
        assert parse_text(document) == expected
