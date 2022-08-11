from search import Search


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


geom = {
    "type": "Polygon",
    "coordinates": [
        [
            [128.86421084403992, 37.75191040678909],
            [128.87457489967343, 37.75191040678909],
            [128.87457489967343, 37.764574381819955],
            [128.86421084403992, 37.764574381819955],
            [128.86421084403992, 37.75191040678909],
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
    "config": {"lte": "2022-09-01T00:00:00.000Z"},
}

# filter any images which are more than 50% clouds
cloud_cover_filter = {
    "type": "RangeFilter",
    "field_name": "cloud_cover",
    "config": {"lte": 0.2},
}


asset_filter = {"type": "AssetFilter", "config": ["ortho_analytic_4b_sr"]}

standard = {
    "type": "StringInFilter",
    "config": ["standard"],
    "field_name": "quality_category",
}

# create a filter that combines our geo and date filters
# could also use an "OrFilter"
combined_filter = {
    "type": "AndFilter",
    "config": [
        geometry_filter,
        date_range_filter,
        cloud_cover_filter,
        asset_filter,
        standard,
    ],
}

ss = Search(ITEM_TYPE)
items = ss.get(combined_filter)
print(ss.request)
# print(items.ids)
print(items)
so = Order("api_test", "analytic_sr_udm2", items, stac=True)
# so.tools(geom)
# print(so.request)
# print(so.status())
# so.place()
# print(so.status())
# print(so.cancel())
# print(so.status())
