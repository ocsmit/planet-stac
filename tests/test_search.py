import pytest

from planetstac.search import Search, ItemIds


@pytest.fixture
def search_filter():
    geom = {
        "type": "Polygon",
        "coordinates": [
            [
                [-78.67905020713806, 35.780212341409914],
                [-78.67378234863281, 35.780212341409914],
                [-78.67378234863281, 35.782684221280086],
                [-78.67905020713806, 35.782684221280086],
                [-78.67905020713806, 35.780212341409914],
            ]
        ],
    }

    geometry_filter = {
        "type": "GeometryFilter",
        "field_name": "geometry",
        "config": geom,
    }

    # filter images acquired in a certain date range
    date_range_filter = {
        "type": "DateRangeFilter",
        "field_name": "acquired",
        "config": {
            "gte": "2016-07-01T00:00:00.000Z",
            "lte": "2016-08-01T00:00:00.000Z",
        },
    }

    # filter any images which are more than 50% clouds
    cloud_cover_filter = {
        "type": "RangeFilter",
        "field_name": "cloud_cover",
        "config": {"lte": 0.5},
    }

    # create a filter that combines our geo and date filters
    # could also use an "OrFilter"
    combined_filter = {
        "type": "AndFilter",
        "config": [geometry_filter, date_range_filter, cloud_cover_filter],
    }
    return combined_filter


@pytest.fixture
def item_types():
    return {
        "FAIL": "BAD",
        "PASS": "PSScene",
    }


@pytest.fixture
def valid_items():
    return ItemIds("PSScene", ["20160713_143153_0c2b", "20160706_171548_0c1b"])


def test_item_type(item_types):
    with pytest.raises(ValueError) as _:
        Search(item_types["FAIL"])


def test_search(search_filter, item_types, valid_items):
    search = Search(item_types["PASS"])
    items = search.get(search_filter)
    assert items == valid_items
