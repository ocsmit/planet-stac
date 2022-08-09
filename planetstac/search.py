import requests
from typing import Any, Dict, Union, List
from dataclasses import dataclass
import pprint

if __package__:
    from .item_types import AVAILABLE_ITEM_TYPES
    from .auth import Authenticate
else:
    from item_types import AVAILABLE_ITEM_TYPES
    from auth import Authenticate

SearchRequest = Dict[str, Union[List[str], Dict[str, Any]]]

# NOTIMPLEMENTED
class SearchFilter:
    def __init__(
        self,
        name: str,
        item_type: str,
        geom: List[str],
        assets: Union[List[str], None] = None,
        dates: Union[List[str], None] = None,
    ):
        self._name = name
        self._item_type = item_type
        self._assets = assets
        self._geom = geom
        self._dates = dates

        self._filter_lookup = {
            "geom": "GeometryFilter",
            "assets": "AssetFilter",
            "range": "RangeFilter",
            "date": "DateRangeFilter",
            "number": "NumberInFilter",
            "string": "StringInFilter",
            "update": "UpdateFilter",
        }


AVAILABLE_FILTERS = {
    "geom": ("GeometryFilter", True),
    "asset": ("AssetFilter", False),
    "range": ("RangeFilter", True),
    "date": ("DateRangeFilter", False),
    "number": ("NumberInFilter", True),
    "string": ("StringInFilter", True),
    "update": ("UpdateFilter", True),
    "permission": ("PermissionFilter", False),
    "and": ("AndFilter", False),
    "not": ("NotFilter", False),
    "or": ("OrFilter", False),
}


@dataclass
class Filter:
    type: str
    config: Any
    field_name: Union[str, None] = None


def create_filter(type, config, field_name=None):
    assert type in AVAILABLE_FILTERS.keys(), "Improper filter type"
    pass


# END NOTIMPLEMENTED


@dataclass
class ItemIds:
    """
    simple struct to keep item type and ids
    """

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
    def __init__(self, item_type, filter, **kwargs) -> None:
        """
        Class for searching Planet API

        TODO: Document

        returns
        -------
            items: ItemIds

        """
        # Set up authtication
        super().__init__(**kwargs)

        self._item_type = item_type
        self._request = None
        if self.__validate_item_type() == False:
            raise ValueError("Invalid item type")

        # Construct request and post
        self._request = self.__construct_request(filter)
        response = requests.post(
            "https://api.planet.com/data/v1/quick-search",
            auth=self.authentication,
            json=self._request,
        )
        # Check if request suceeded
        assert response.ok == True, response.text

        # Assign variables based off response
        self._response = response
        self._ids = [feature["id"] for feature in response.json()["features"]]

    def __validate_item_type(self) -> bool:
        """
        Private method for validating item types
        """
        if self._item_type not in AVAILABLE_ITEM_TYPES:
            return False
        return True

    def __construct_request(self, filter) -> SearchRequest:
        """
        Private method to construct request
        """
        search_request = {
            "item_types": [self._item_type],
            "filter": filter,
        }
        return search_request

    @property
    def items(self) -> ItemIds:
        return ItemIds(self._item_type, self._ids)

    @property
    def response(self) -> requests.Response:
        return self._response

    @property
    def item_type(self) -> str:
        return self._item_type

    @property
    def request(self) -> Union[SearchRequest, None]:
        return self._request
