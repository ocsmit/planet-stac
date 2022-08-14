import json
import os
from typing import Dict, List, Union, Any
from dataclasses import dataclass
import warnings

import requests
from requests.models import Response

if __package__:
    from .consts import ORDER_URL, HEADERS
    from .search import ItemIds, search
    from .auth import authenticate, Authentication
else:
    from consts import ORDER_URL, HEADERS
    from search import ItemIds, search
    from auth import authenticate, Authentication


@dataclass
class PlanetOrder:
    id: str
    url: str
    status: str
    authentication: Authentication
    response: Dict[str, Union[str, Any]]


def create_PlanetOrder(
    response: Dict[str, Union[str, Any]],
    authentication: Union[None, Authentication],
    **kwargs,
) -> PlanetOrder:
    if authentication == None:
        authentication = authenticate(**kwargs)
    if not isinstance(authentication, Authentication):
        raise Exception("Improper authentication provided")

    po = PlanetOrder(
        id=response["id"],
        url=ORDER_URL,
        status=response["state"],
        authentication=authentication,
        response=response,
    )

    return po


update_PlanetOrder = create_PlanetOrder


def set_tools(self, geom):
    # What is best practice? Have tools defined at initialization as
    # parameters or call seperatly to update the request?
    tools = {}
    tools["tools"] = [{"clip": {"aoi": geom}}]
    return tools


def construct_order_request(
    name,
    product_bundle,
    items: ItemIds,
    tools=None,
    stac: bool = False,
) -> Dict[str, Union[str, Any]]:
    """
    construct request based of init parameters
    """
    req = {}
    req["name"] = name
    req["products"] = [
        {
            "item_ids": items.ids,
            "item_type": items.item_type,
            "product_bundle": product_bundle,
        }
    ]
    if stac == True:
        req["metadata"] = {"stac": {}}

    req["tools"] = tools
    return req


def check_order_response(response: Response) -> None:
    if response.status_code == 429:
        raise Exception("Rate limit error")
    elif response.ok != True:
        raise Exception(
            f"ERROR: unsuccessful request, Got response code"
            f"{response.status_code}, reason is {response.reason}"
        )


def place_order(order_request: Dict[str, Union[str, Any]], **kwargs) -> PlanetOrder:
    authentication = authenticate(**kwargs)
    # Add logic to check if valid request format
    response = requests.post(
        ORDER_URL,
        data=json.dumps(order_request),
        auth=authentication.auth,
        headers=HEADERS,
    )

    check_order_response(response)

    return create_PlanetOrder(response.json(), authentication)


def order_status(order: PlanetOrder, **kwargs) -> PlanetOrder:
    authentication = order.authentication
    order.status = requests.get(order.url, auth=authentication.auth).json()["state"]
    return order


def get_order(order: Union[str, PlanetOrder], **kwargs) -> PlanetOrder:
    if isinstance(order, str):
        authentication = authenticate(**kwargs)
        order_url = f"{ORDER_URL}/{order}"
    elif isinstance(order, PlanetOrder):
        authentication = order.authentication
        order_url = order.url
    else:
        raise Exception("Provide either order id or PlanetOrder object")

    response = requests.get(order_url, auth=authentication.auth)
    check_order_response(response)

    # Create/Update PlanetOrder object
    order = update_PlanetOrder(response.json(), authentication)
    return order


def cancel(order: Union[str, PlanetOrder], **kwargs) -> PlanetOrder:
    """
    Cancel order that has been placed.
    NOTE: If order request has reached "running" state then it can
          no longer be canceled
    """
    if isinstance(order, str):
        authentication = authenticate(**kwargs)
        order_url = f"{ORDER_URL}/{order}"
    elif isinstance(order, PlanetOrder):
        authentication = order.authentication
        order_url = order.url
    else:
        raise Exception("Provide either order id or PlanetOrder object")

    response = requests.get(order_url, auth=authentication.auth)
    check_order_response(response)
    # Create/Update PlanetOrder object
    order = update_PlanetOrder(response.json(), authentication)

    # Check if order has been placed
    if order.status == "running":
        warnings.warn(
            UserWarning("Cancel Warning, order status has already started running")
        )
    else:
        response = requests.put(order_url, auth=authentication.auth)
        assert response.ok == True, response.text
        order.status = "canceled"

    return order
