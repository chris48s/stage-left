import pytest

from stage_left import ParseError, parse_text
from stage_left.types import Group, Item, State

valid_items = """[ ] Open
[x] Checked
[@] Ongoing
[~] Obsolete
[?] In Question
[ ] Do this
[ ]   Do this
[ ]
[ ] 
[ ]       
[ ] This is a longer ...
    description text
[ ] And this one ...
    is even ...
    longer
[ ] The following is just ...
    [ ] description text
[x] These lines ...
    should all ...
    look the same
[ ] This has some ...
       more spaces
[ ] And this one ...
             as well
[ ] And this one uses a\r\n    Windows linebreak
"""  # noqa:W291

no_indent = """[ ] The next line is ...
invalid"""

insufficient_indent1 = """[ ] The next line is ...
 invalid"""

insufficient_indent2 = """[ ] The next line is ...
   invalid"""

tab_indent = """[ ] The next line is ...
	invalid (it’s a tab)"""  # noqa:W191,E101

invalid_items = [
    "[*] Invalid",
    "[o] Invalid",
    "[X] Invalid (uppercase)",
    "[ ] Invalid (non-breaking space)",
    "[] Invalid",
    "[  ] Invalid",
    "[ x ] Invalid",
    "[@@] Invalid",
    " [x] Invalid",
    "    [x] Invalid",
    "[ ]Invalid",
    "[ ]! Invalid",
    "[ ]. Invalid",
    "[ ]!!. Invalid",
    "[ ]#invalid",
    "[ ]->2022-02-16 Invalid",
    no_indent,
    insufficient_indent1,
    insufficient_indent2,
    tab_indent,
]


def test_items_valid():
    expected = [
        Group(
            items=[
                Item(
                    state=State.OPEN,
                    description="Open",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.CHECKED,
                    description="Checked",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.ONGOING,
                    description="Ongoing",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.OBSOLETE,
                    description="Obsolete",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.IN_QUESTION,
                    description="In Question",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.OPEN,
                    description="Do this",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.OPEN,
                    description="  Do this",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.OPEN,
                    description="",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.OPEN,
                    description="",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.OPEN,
                    description="      ",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.OPEN,
                    description="This is a longer ...\ndescription text",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.OPEN,
                    description="And this one ...\nis even ...\nlonger",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.OPEN,
                    description="The following is just ...\n[ ] description text",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.CHECKED,
                    description="These lines ...\nshould all ...\nlook the same",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.OPEN,
                    description="This has some ...\n   more spaces",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.OPEN,
                    description="And this one ...\n         as well",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
                Item(
                    state=State.OPEN,
                    description="And this one uses a\nWindows linebreak",
                    tags=set(),
                    priority=0,
                    due_date=None,
                ),
            ],
            title="",
        )
    ]
    assert parse_text(valid_items) == expected


@pytest.mark.parametrize("item", invalid_items)
def test_items_invalid(item):
    with pytest.raises(ParseError):
        parse_text(item)
