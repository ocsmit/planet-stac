import pytest
import time
from planetstac.order import (
    PlanetOrder,
    create_PlanetOrder,
    construct_order_request,
    place_order,
    set_tools,
    cancel_order,
)
from planetstac import ItemIds

from .helpers import search_filter, IDS, ITEMTYPE, PRODUCT_BUNDLE, GEOM


@pytest.fixture
def correct_tools():
    tools = [
        {
            "clip": {"aoi": GEOM},
        },
    ]

    return tools


def test_tools(correct_tools):
    tools = set_tools(GEOM)
    assert tools == correct_tools


@pytest.fixture()
def correct_order_request():
    req = {
        "name": "api-test",
        "products": [
            {
                "item_ids": IDS,
                "item_type": ITEMTYPE,
                "product_bundle": PRODUCT_BUNDLE,
            }
        ],
        "metadata": {
            "stac": {},
        },
        "tools": [
            {
                "clip": {"aoi": GEOM},
            },
        ],
    }
    return req


def test_order_construct(correct_order_request, correct_tools):
    req = construct_order_request(
        name="api-test",
        product_bundle=PRODUCT_BUNDLE,
        items=ItemIds(ITEMTYPE, IDS),
        tools=correct_tools,
        stac=True,
    )
    assert req == correct_order_request


@pytest.mark.skip("Only test ordering sparingly")
def test_place_order(correct_order_request):
    time.sleep(1.5)
    order = place_order(correct_order_request, dry=False)
    assert order.status == "queued"
    order = cancel_order(order)
    assert order.status == "canceled"

    # assert order.status == "canceled"
