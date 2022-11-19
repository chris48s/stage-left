import pytest

from stage_left.parser import classify_lines, parse_item
from stage_left.types import Tag

valid_multi_line_tags = """[ ] #Actually, it #has a #LOT.
    Even on the #next-line!"""

valid_tags = [
    ["[ ] #tag", {Tag(value="tag")}],
    ["[ ] #T-A-G", {Tag(value="T-A-G")}],
    ["[ ] #--tag--", {Tag(value="--tag--")}],
    ["[ ] #__tag__", {Tag(value="__tag__")}],
    ["[ ] #t_a_g", {Tag(value="t_a_g")}],
    ["[ ] #123", {Tag(value="123")}],
    ["[ ] #___", {Tag(value="___")}],
    ["[ ] #---", {Tag(value="---")}],
    ["[ ] #1t2a3g", {Tag(value="1t2a3g")}],
    ["[ ] #täg", {Tag(value="täg")}],
    ["[ ] #今日は", {Tag(value="今日は")}],
    ["[ ] #გამარჯობა", {Tag(value="გამარჯობა")}],
    ["[ ] This #text contains #tags", {Tag(value="text"), Tag(value="tags")}],
    [
        valid_multi_line_tags,
        {
            Tag(value="Actually"),
            Tag(value="has"),
            Tag(value="LOT"),
            Tag(value="next-line"),
        },
    ],
    ["[ ] This is a #tag.", {Tag(value="tag")}],
    ["[ ] Tags: #tag1/#tag2", {Tag(value="tag1"), Tag(value="tag2")}],
    ["[ ] #t-a-g!", {Tag(value="t-a-g")}],
    ["[ ] #--tag--?", {Tag(value="--tag--")}],
    ["[ ] #--tag--:text", {Tag(value="--tag--")}],
    ["[ ] (#tag)", {Tag(value="tag")}],
    ["[ ] #tag🥳", {Tag(value="tag")}],
    ["[ ] #tag=value", {Tag(key="tag", value="value")}],
    ["[ ] #t-a-g=v-a-l-u-e", {Tag(key="t-a-g", value="v-a-l-u-e")}],
    ["[ ] #国=日本", {Tag(key="国", value="日本")}],
    ["[ ] #tag=", {Tag(key="tag", value="")}],
    ['[ ] #tag=""', {Tag(key="tag", value="")}],
    ["[ ] #tag=''", {Tag(key="tag", value="")}],
    ['[ ] #tag="v a l u e"', {Tag(key="tag", value="v a l u e")}],
    ["[ ] #tag='v!a.l?u+e'", {Tag(key="tag", value="v!a.l?u+e")}],
    ["[ ] #tag='foo'bar", {Tag(key="tag", value="foo")}],
    ["[ ] #tag='foo'-bar", {Tag(key="tag", value="foo")}],
    ["[ ] #tag='foo'!!", {Tag(key="tag", value="foo")}],
    ['[ ] (#tag="bar")', {Tag(key="tag", value="bar")}],
    [
        '[ ] #tag1="foo" #tag2="bar"',
        {Tag(key="tag1", value="foo"), Tag(key="tag2", value="bar")},
    ],
    [
        "[ ] #tag1='foo' #tag2='bar'",
        {Tag(key="tag1", value="foo"), Tag(key="tag2", value="bar")},
    ],
    [
        "[ ] #This #item #has=\"all\" #the=\"different\" #tag='formats' #in='it' #one=way #or=another",
        {
            Tag(value="This"),
            Tag(value="item"),
            Tag(key="has", value="all"),
            Tag(key="the", value="different"),
            Tag(key="tag", value="formats"),
            Tag(key="in", value="it"),
            Tag(key="one", value="way"),
            Tag(key="or", value="another"),
        },
    ],
]

invalid_multi_line_tags = """[ ] #tag="hello
    World!\""""

invalid_tags = [
    ["[ ] Not a tag: #", set()],
    ["[ ] #tag='It\\'s great", {Tag(key="tag", value="It\\")}],
    ['[ ] #tag="v a l u e', {Tag(key="tag", value="")}],
    ["[ ] #tag=\"v a l u e'", {Tag(key="tag", value="")}],
    [invalid_multi_line_tags, {Tag(key="tag", value="")}],
]


@pytest.mark.parametrize("item", valid_tags)
def test_tags_valid(item):
    input_, expected = item
    parsed_item = parse_item(classify_lines([input_]))
    assert parsed_item.tags == expected


@pytest.mark.parametrize("item", invalid_tags)
def test_tags_invalid(item):
    input_, expected = item
    parsed_item = parse_item(classify_lines([input_]))
    assert parsed_item.tags == expected
