from stage_left.types import Group, Item, Line, LineType, ParseError, State

ALLOWED_ITEM_STARTS = [f"[{state.value}] " for state in State]
ALLOWED_ITEM_LINES = [s.strip() for s in ALLOWED_ITEM_STARTS]


def classify_line(line, prev_line_type, index):
    line_type = LineType.ERROR

    line_start = line[0:4]
    if line_start in ALLOWED_ITEM_STARTS or line in ALLOWED_ITEM_LINES:
        line_type = LineType.ITEM_START
    elif len(line.strip()) == 0:
        line_type = LineType.WHITESPACE
    elif line_start == "    " and prev_line_type in [
        LineType.ITEM_START,
        LineType.ITEM_CONTINUATION,
    ]:
        line_type = LineType.ITEM_CONTINUATION
    elif (
        line_start.lstrip() == line_start
        and not line_start.startswith("[")
        and (prev_line_type == LineType.WHITESPACE or not prev_line_type)
    ):
        line_type = LineType.GROUP_TITLE

    if line_type == LineType.ERROR:
        raise ParseError(f"Error on line {index}:\n{line}")

    return Line(line_type=line_type, text=line)


def classify_lines(lines):
    classified_lines = []
    for index, line in enumerate(lines):
        prev_line_type = None
        if index > 0:
            prev_line_type = classified_lines[index - 1].line_type
        classified_lines.append(classify_line(line, prev_line_type, index))
    return classified_lines


def parse_tags(text):
    return []


def parse_priority(text):
    head, *_ = text.split(" ")

    if len(head.strip("!.")) > 0:
        return 0

    if len(head) > 0 and head[0] == ".":
        # left-padded
        stripped = head.lstrip(".")
        if "." in stripped:
            return 0
        return stripped.count("!")

    if len(head) > 0 and head[-1] == ".":
        # right-padded
        stripped = head.rstrip(".")
        if "." in stripped:
            return 0
        return stripped.count("!")

    if "." in head:
        # neither left-padded nor night-padded
        # but contains padding character (invalid)
        return 0

    return head.count("!")


def parse_due_date(text):
    return None


def parse_item(lines):
    line, *tail = lines
    text = line.text[4:]
    for continuation_line in tail:
        if continuation_line.line_type != LineType.ITEM_CONTINUATION:
            break
        text += "\n" + continuation_line.text[4:]
    # TODO: extract tags and due date
    tags = parse_tags(text)
    priority = parse_priority(line.text[4:])
    due_date = parse_due_date(text)
    return Item(
        state=State(line.text[1]),
        description=text,
        tags=tags,
        priority=priority,
        due_date=due_date,
    )


def parse_lines(lines):
    groups = []
    current_group = None

    for index, line in enumerate(lines):
        if (
            line.line_type == LineType.WHITESPACE
            or line.line_type == LineType.ITEM_CONTINUATION
        ):
            continue

        if line.line_type == LineType.GROUP_TITLE:
            current_group = Group(title=line.text)
            groups.append(current_group)
            continue
        elif line.line_type == LineType.ITEM_START and index == 0:
            current_group = Group(title="")
            groups.append(current_group)
        elif (
            line.line_type == LineType.ITEM_START
            and index > 0
            and lines[index - 1].line_type == LineType.WHITESPACE
        ):
            current_group = Group(title="")
            groups.append(current_group)

        if line.line_type == LineType.ITEM_START:
            current_group.items.append(parse_item(lines[index:]))

    return groups


def parse_text(text):
    return parse_lines(classify_lines(text.splitlines()))


def parse_file(file_):
    # TODO
    pass
