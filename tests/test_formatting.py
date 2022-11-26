import pytest

from stage_left import parse_text

items = [
    "[ ] Do a thing",
    # tags
    "[ ] Do a #value thing",
    "[ ] Do a#value thing",
    "[ ] Do a #key=value thing",
    "[ ] Do a #key='value' thing",
    '[ ] Do a #key="value" thing',
    "[ ] Do a #value #key=value thing\n    #key='value' #key=\"value\"",
    # priority and tags
    "[ ] !!. Do a #value thing",
    "[ ] !!. Do a#value thing",
    "[ ] !!. Do a #key=value thing",
    "[ ] !!. Do a #key='value' thing",
    '[ ] !!. Do a #key="value" thing',
    "[ ] !!. Do a #value #key=value thing\n    #key='value' #key=\"value\"",
    # date and tags
    "[ ] Do a #value thing -> 2022-01-31",
    "[ ] Do a#value thing -> 2022-01-31",
    "[ ] Do a #key=value thing -> 2022-01-31",
    "[ ] Do a #key='value' thing -> 2022-01-31",
    '[ ] Do a #key="value" thing (-> 2022-01-31)',
    "[ ] Do a #value #key=value thing -> 2022-01-31\n    #key='value' #key=\"value\"",
    # priority and date
    "[ ] !!. Do a thing -> 2022-01-31",
    "[ ] !!. Do a thing (-> 2022-01-31)",
    # priority, date and tags
    "[ ] !!. Do a #value thing -> 2022-01-31",
    "[ ] !!. Do a#value thing -> 2022-01-31",
    "[ ] !!. Do a #key=value thing -> 2022-01-31",
    "[ ] !!. Do a #key='value' thing -> 2022-01-31",
    '[ ] !!. Do a #key="value" thing (-> 2022-01-31)',
    "[ ] !!. Do a #value #key=value thing -> 2022-01-31\n    #key='value' #key=\"value\"",
]


@pytest.mark.parametrize("item_text", items)
def test_strip_priority(item_text):
    item = parse_text(item_text)[0].items[0]
    assert item.format_description(
        normalize_whitespace=True,
        with_priority=False,
        with_tags=True,
        with_due_date=True,
    ).startswith("Do a")


@pytest.mark.parametrize("item_text", items)
def test_strip_due_date(item_text):
    item = parse_text(item_text)[0].items[0]
    assert "-> 2022-01-31" not in item.format_description(
        normalize_whitespace=True,
        with_priority=True,
        with_tags=True,
        with_due_date=False,
    )


@pytest.mark.parametrize("item_text", items)
def test_strip_tags(item_text):
    item = parse_text(item_text)[0].items[0]
    assert "Do a thing" in item.format_description(
        normalize_whitespace=True,
        with_priority=True,
        with_tags=False,
        with_due_date=True,
    )


@pytest.mark.parametrize("item_text", items)
def test_strip_everything(item_text):
    item = parse_text(item_text)[0].items[0]
    assert (
        item.format_description(
            normalize_whitespace=True,
            with_priority=False,
            with_tags=False,
            with_due_date=False,
        )
        == "Do a thing"
    )


@pytest.mark.parametrize("item_text", items)
def test_do_nothing(item_text):
    item = parse_text(item_text)[0].items[0]
    assert (
        item.format_description(
            normalize_whitespace=False,
            with_priority=True,
            with_tags=True,
            with_due_date=True,
        )
        == item.description
    )
