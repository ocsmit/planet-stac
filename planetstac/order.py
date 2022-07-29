import json
import os
from typing import Dict, List, Union

import requests

if __package__:
    from .search import Search, ItemIds
    from .auth import Authenticate
else:
    from search import Search, ItemIds
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

        self._name = name
        self._product_bundle = product_bundle
        self._items = items

        # Required for auth
        self._url = "https://api.planet.com/compute/ops/orders/v2"

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

    def __construct_request(self) -> Dict[str, Union[str, List[str]]]:
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

    def place(self) -> None:
        headers = {"content-type": "application/json"}
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
        self.__taste_of_order()
        response = requests.put(self._order_url, auth=self._auth)
        assert response.ok == True, response.text
        self._state = 0  # set to canceled

    def status(self) -> str:
        if self._order_url == self._null:
            return "unplaced"

        return requests.get(self._order_url, auth=self._auth).json()["state"]

    @property
    def request(self):
        return self._request

    @property
    def order_url(self):
        return self._order_url

    def __taste_of_order(self) -> None:
        if self._order_url == self._null:
            raise ValueError("Order has not been placed")
        else:
            # Order has been placed
            pass


ITEM_TYPE = "PSScene"

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
    "config": {"gte": "2016-07-01T00:00:00.000Z", "lte": "2016-08-01T00:00:00.000Z"},
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


ss = Search(ITEM_TYPE)
items = ss.get(combined_filter)
# print(items)
so = Order("api_test", "analytic_udm2", items)
print(so.status())
# so.place()
# print(so.status())
# print(so.cancel())
# print(so.status())
