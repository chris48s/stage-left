from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Optional, Set


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
    Meaning of the Item

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
