import json
import os
import pathlib
import time
from dataclasses import dataclass
from typing import List

import requests
from requests.auth import HTTPBasicAuth
from search import Search


from search import ItemIds


class Order:
    def __init__(self, name: str, product_bundle: str, items: ItemIds) -> None:
        self._name = name
        self._product_bundle = product_bundle
        self._items = items

        # Required for auth
        self._url = "https://api.planet.com/compute/ops/orders/v2"
        self._auth = HTTPBasicAuth(os.getenv("PL_API_KEY"), "")

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

    def __construct_request(self):
        req = {}
        req["name"] = self._name
        req["products"] = [
            {
                "item_ids": self._items.ids,
                "item_type": self._items.item_type,
                "product_bundle": self._product_bundle,
            }
        ]
        return req

    def place(self):
        headers = {"content-type": "application/json"}
        response = requests.post(
            self._url,
            data=json.dumps(self._request),
            auth=self._auth,
            headers=headers,
        )
        print(response)
        assert response.ok == True, f"{response.status_code} {response.text}"
        self._state = 1  # Set to running

        self._response = response
        order_id = response.json()["id"]
        order_url = f"{orders_url}/{order_id}"
        self._order_url = order_url

    def cancel(self):
        self.__taste_of_order()
        response = requests.put(self._order_url, auth=self._auth)
        assert response.status_code == 409, response.text

        self._state = 0  # set to canceled

    def status(self):
        self.__taste_of_order()
        return requests.get(self._order_url, auth=self._auth).json()["state"]

    @property
    def request(self):
        return self._request

    @property
    def order_url(self):
        return self._order_url

    def __taste_of_order(self):
        if self._order_url == self._null:
            raise ValueError("Order has not been placed")
        elif self._state == 0:
            raise ValueError("Order has been canceled")
        else:
            # Order has been placed
            pass


ITEM_TYPE = "PSScene"

ss = Search(ITEM_TYPE, PLANET_API_KEY)
items = ss.get(combined_filter)
print(ss.item_type)
so = Order("simple", "analytic_udm2", items)
req = {
    "name": "simple order",
    "products": [
        {
            "item_ids": ["20151119_025740_0c74", "20151119_025741_0c74"],
            "item_type": "PSScene",
            "product_bundle": "analytic_udm2",
        }
    ],
}

print(json.dumps(so.request))
print(json.dumps(req))
so.place()
print(so.status())
print(so.cancel())
