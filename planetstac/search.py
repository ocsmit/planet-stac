import requests
from typing import Union, List
from dataclasses import dataclass
import pprint

if __package__:
    from .item_types import AVAILABLE_ITEM_TYPES
    from .auth import Authenticate
else:
    from item_types import AVAILABLE_ITEM_TYPES
    from auth import Authenticate


class SearchFilter:
    def __init__(
        self,
        name: str,
        item_type: str,
        assets: Union[List[str], None] = None,
        geom: Union[List[str], None] = None,
    ):
        self._name = name
        self._item_type = item_type
        self._assets = assets
        self._geom = geom

        self._filter_lookup = {
            "geom": "GeometryFilter",
            "assets": "AssetFilter",
            "range": "RangeFilter",
            "date": "DateRangeFilter",
            "number": "NumberInFilter",
            "string": "StringInFilter",
            "update": "UpdateFilter",
        }


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
    "config": {"gte": "2018-08-30T00:00:00.000Z", "lte": "2018-09-01T00:00:00.000Z"},
}

# filter any images which are more than 50% clouds
cloud_cover_filter = {
    "type": "RangeFilter",
    "field_name": "cloud_cover",
    "config": {"lte": 0.5},
}


asset_filter = {"type": "AssetFilter", "config": ["ortho_analytic_4b_sr"]}

# create a filter that combines our geo and date filters
# could also use an "OrFilter"
combined_filter = {
    "type": "AndFilter",
    "config": [geometry_filter, date_range_filter, cloud_cover_filter, asset_filter],
}


@dataclass
class ItemIds:
    item_type: str
    ids: List[str]

    def __str__(self) -> str:
        return pprint.pformat(
            {
                "item_type": self.item_type,
                "ids": self.ids,
                "count": len(self.ids),
            },
            depth=1,
            sort_dicts=False,
        )


class Search(Authenticate):
    def __init__(
        self,
        item_type,
        assets: Union[List[str], None] = None,
        geom: Union[List[str], None] = None,
        **kwargs
    ) -> None:
        # Set up authtication
        super().__init__(**kwargs)

        self._item_type = item_type
        self._assets = assets
        self._geom = geom
        if self.__validate_item_type() == False:
            raise ValueError("Invalid item type")
        pass

    def get(self, filter=None) -> ItemIds:
        req = self.__construct_request(filter)
        response = requests.post(
            "https://api.planet.com/data/v1/quick-search",
            auth=self.authentication,
            json=req,
        )
        assert response.ok == True, response.text
        self._response = response
        self._ids = [feature["id"] for feature in response.json()["features"]]
        return ItemIds(self._item_type, self._ids)

    def __validate_item_type(self) -> bool:
        if self._item_type not in AVAILABLE_ITEM_TYPES:
            return False
        return True

    def __construct_request(self, filter) -> dict:
        search_request = {
            "item_types": [self._item_type],
        }
        if filter is not None:
            search_request["filter"] = filter

        return search_request

    @property
    def ids(self) -> Union[None, List[str]]:
        return self._ids

    @property
    def response(self):
        return self._response

    @property
    def item_type(self):
        return self._item_type
