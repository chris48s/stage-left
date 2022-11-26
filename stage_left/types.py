from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Optional, Set

from stage_left import formatters


class State(Enum):
    """
    State of an Item

    :ref: https://github.com/jotaen/xit/blob/main/Specification.md#checkbox
    """

    OPEN = " "
    CHECKED = "x"
    ONGOING = "@"
    OBSOLETE = "~"


@dataclass(frozen=True)
class Tag:
    """
    An annotation for categorising or filtering the data

    :ref: https://github.com/jotaen/xit/blob/main/Specification.md#tag
    """

    value: str = ""
    key: Optional[str] = None


@dataclass()
class Item:
    """
    An entry in a checklist or todo list

    :ref: https://github.com/jotaen/xit/blob/main/Specification.md#item
    """

    state: State

    description: str
    """
    Meaning of the Item. The :attr:`Item.description` property stores the raw item text,
    but formatting options are available via :meth:`Item.format_description`.

    :ref: https://github.com/jotaen/xit/blob/main/Specification.md#description
    """

    tags: Set[Tag] = field(default_factory=set)

    priority: int = 0
    """
    Int represation of the Item importance

    :ref: https://github.com/jotaen/xit/blob/main/Specification.md#priority
    """

    due_date: Optional[date] = None
    """
    Date object representing the item due date.
    Due dates specified using the numbered week syntax e.g: `2022-W01` are
    parsed assuming Monday is the first day of the week. All days in a new
    year preceding the first Monday are considered to be in week 0 (`W00`).

    :ref: https://github.com/jotaen/xit/blob/main/Specification.md#due-date
    """

    def format_description(
        self,
        *,
        normalize_whitespace: bool = False,
        with_priority: bool = True,
        with_tags: bool = True,
        with_due_date: bool = True
    ) -> str:
        """
        Output a formatted version of the item description.

        Args:
            normalize_whitespace:
                Remove duplicate whitespace from the output item description
            with_priority: Include priority in the output item description
            with_tags: Include tags in the output item description
            with_due_date: Include due date in the output item description
        """

        desc = self.description

        if not with_priority and self.priority > 0:
            desc = " ".join(desc.split(" ")[1:])

        if not with_tags and len(self.tags) > 0:
            desc = formatters.strip_tags(desc)

        if not with_due_date and self.due_date:
            desc = formatters.strip_due_date(desc)

        if normalize_whitespace:
            desc = " ".join(desc.split())

        return desc


@dataclass()
class Group:
    """
    A group of one or more Items

    :ref: https://github.com/jotaen/xit/blob/main/Specification.md#group
    """

    title: Optional[str]
    items: List[Item] = field(default_factory=list)


class LineType(Enum):
    ERROR = 0
    GROUP_TITLE = 1
    ITEM_START = 2
    ITEM_CONTINUATION = 3
    WHITESPACE = 4


@dataclass()
class Line:
    line_type: LineType
    text: str


class ParseError(Exception):
    pass
