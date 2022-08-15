import pytest

from planetstac.search import search, ItemIds

from .helpers import search_filter, item_types, valid_items


def test_item_type(item_types, search_filter):
    with pytest.raises(AssertionError) as _:
        search(item_types["FAIL"], search_filter)


def test_search(search_filter, item_types, valid_items):
    ss = search(item_types["PASS"], search_filter)
    assert ss == valid_items
