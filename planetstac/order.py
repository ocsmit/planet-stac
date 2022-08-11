import json
import os
from typing import Dict, List, Union, Any
from dataclasses import dataclass
import warnings

import requests

if __package__:
    from .consts import ORDER_URL
    from .search import ItemIds
    from .auth import Authenticate
else:
    from consts import ORDER_URL
    from search import ItemIds
    from auth import Authenticate


class Order(Authenticate):
    def __init__(
        self,
        name: str,
        product_bundle: str,
        items: ItemIds,
        **kwargs,
    ) -> None:
        # Initalize authenication
        super().__init__(**kwargs)

        # Initialize params for request
        self._name = name
        self._product_bundle = product_bundle
        self._items = items
        self._tool_req = None
        self._stac = kwargs.get("stac", False)

        # Planet API order endpoint
        self._url = ORDER_URL

        # Create JSON to request order
        self._request = self.__construct_request()

        # States:
        #    0 = Order canceled
        #    1 = Order running
        self._state = 0

        # Set to NULL Byte to initialize, requests only take types string
        # or bytes
        self._null = b"\x00"
        self._order_url = self._null

        pass

    def __construct_request(self) -> Dict[str, Union[str, Any]]:
        """
        construct request based of init parameters
        """
        req = {}
        req["name"] = self._name
        req["products"] = [
            {
                "item_ids": self._items.ids,
                "item_type": self._items.item_type,
                "product_bundle": self._product_bundle,
            }
        ]
        if self._stac == True:
            req["metadata"] = {"stac": {}}

        # Initalize tools as empty entry
        req["tools"] = self._tool_req
        return req

    def place(self) -> None:
        headers = {"content-type": "application/json"}

        # Send request
        response = requests.post(
            self._url,
            data=json.dumps(self._request),
            auth=self.authentication,
            headers=headers,
        )
        assert response.ok == True, f"{response.status_code} {response.text}"

        if response.status_code == 429:
            raise Exception("Rate limit error")
        elif response.ok != True:
            print(
                f"ERROR: unsuccessful request, Got response code"
                f"{response.status_code}, reason is {response.reason}"
            )
        self._state = 1  # Set to running

        self._response = response
        order_id = response.json()["id"]
        order_url = f"{self._url}/{order_id}"
        self._order_url = order_url

    def cancel(self) -> None:
        """
        Cancel order that has been placed.
        NOTE: If order request has reached "running" state then it can
              no longer be canceled
        """
        # Check if order has been placed
        self.__taste_of_order()
        if self.status() == "running":
            warnings.warn(
                UserWarning("Cancel Warning, order status has already started running")
            )
        else:
            response = requests.put(self._order_url, auth=self.authentication)
            assert response.ok == True, response.text
            self._state = 0  # set to canceled

    def status(self) -> str:
        if self._order_url == self._null:
            return "unplaced"

        return requests.get(self._order_url, auth=self.authentication).json()["state"]

    def tools(self, geom):
        # What is best practice? Have tools defined at initialization as
        # parameters or call seperatly to update the request?
        self._tool_req = []
        self._request["tools"] = [{"clip": {"aoi": geom}}]

    def __taste_of_order(self) -> None:
        if self._order_url == self._null:
            raise ValueError("Order has not been placed")
        else:
            # Order has been placed
            pass

    @property
    def order_url(self):
        return self._order_url
