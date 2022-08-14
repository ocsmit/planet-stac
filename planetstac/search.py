import requests
from typing import Any, Dict, Union, List
from dataclasses import dataclass
import pprint
from typing import NamedTuple

if __package__:
    from .consts import AVAILABLE_ITEM_TYPES, SEARCH_URL
    from .auth import Authentication, authenticate
else:
    from consts import AVAILABLE_ITEM_TYPES, SEARCH_URL
    from auth import Authentication, authenticate

SearchRequest = Dict[str, Union[List[str], Dict[str, Any]]]


@dataclass(frozen=True)
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


def validate_item_type(item_type: str) -> bool:
    """
    Private func for validating item types
    """
    if item_type not in AVAILABLE_ITEM_TYPES:
        return False
    return True


def construct_search_request(item_type: str, filter) -> SearchRequest:
    """
    Private method to construct request
    """
    search_request = {
        "item_types": [item_type],
        "filter": filter,
    }
    return search_request


def search(item_type: str, filter, **kwargs) -> ItemIds:
    authentication = authenticate(**kwargs)

    assert validate_item_type(item_type) == True, ValueError("Invalid item type")

    request = construct_search_request(item_type, filter)
    response = requests.post(
        SEARCH_URL,
        auth=authentication.auth,
        json=request,
    )

    assert response.ok == True, response.text
    ids = [feature["id"] for feature in response.json()["features"]]

    return ItemIds(item_type, ids)
