# order = response.json()["orders"]
orders_url = "https://api.planet.com/compute/ops/orders/v2"

headers = {"content-type": "application/json"}

# request = {
#        "name": "Gangneung",
#        prooducts

geom = {
    "type": "Polygon",
    "coordinates": [
        [
            [488.86908173561096, 37.75541378624299],
            [488.87455344200134, 37.75541378624299],
            [488.87455344200134, 37.758577712772066],
            [488.86908173561096, 37.758577712772066],
            [488.86908173561096, 37.75541378624299],
        ]
    ],
}


geom_filter = {
    "type": "GeometryFilter",
    "field_name": "geometry",
    "config": geom,
}

date_range_filter = {
    "type": "DateRangeFilter",
    "field_name": "acquired",
    "config": {"gte": "2020-08-31T00:00:00.000Z", "lte": "2020-09-04T00:00:00.000Z"},
}

# only get images which have <50% cloud coverage
cloud_cover_filter = {
    "type": "RangeFilter",
    "field_name": "cloud_cover",
    "config": {"lte": 0.5},
}

# combine our geo, date, cloud filters
combined_filter = {
    "type": "AndFilter",
    "config": [geom_filter, date_range_filter, cloud_cover_filter],
}
