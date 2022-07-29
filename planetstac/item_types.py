#!/usr/bin/env python3

from typing import List, Union
from dataclasses import dataclass

AVAILABLE_ITEM_TYPES = [
    "PSScene",
    "PSScene3Band",
    "PSScene4Band",
    "PSOrthoTile",
    "REOrthoTile",
    "REScene",
    "SkySatScene",
    "SkySatCollect",
    "SkySatVideo",
    "Landsat8L1G",
    "Sentinel2L1C",
]


def validate_itemtype(item_type):
    if item_type not in AVAILABLE_ITEM_TYPES:
        return 0
    return 1


# https://developers.planet.com/docs/apis/data/items-assets/#item-types
class ItemType:
    def __init__(self, item_type: str) -> None:
        self.item_type = item_type
        self.available_item_types = [
            "PSScene",
            "PSScene3Band",
            "PSScene4Band",
            "PSOrthoTile",
            "REOrthoTile",
            "REScene",
            "SkySatScene",
            "SkySatCollect",
            "SkySatVideo",
            "Landsat8L1G",
            "Sentinel2L1C",
        ]
        assert self.__validate() == 1, "Invalid item type"

    def __validate(self) -> Union[str, int]:
        if self.item_type not in self.available_item_types:
            return 0
        return 1
