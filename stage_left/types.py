from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


class State(Enum):
    OPEN = " "
    CHECKED = "x"
    ONGOING = "@"
    OBSOLETE = "~"


class LineType(Enum):
    ERROR = 0
    GROUP_TITLE = 1
    ITEM_START = 2
    ITEM_CONTINUATION = 3
    WHITESPACE = 4


@dataclass()
class Group:
    title: Optional[str]
    items: list = field(default_factory=list)


@dataclass()
class Item:
    state: State
    description: str
    tags: set = field(default_factory=set)
    priority: int = 0
    due_date: Optional[date] = None


@dataclass(frozen=True)
class Tag:
    value: Optional[str] = None
    key: Optional[str] = None


@dataclass()
class Line:
    line_type: LineType
    text: str


class ParseError(Exception):
    pass
