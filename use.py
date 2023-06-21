
if __name__ == "__main__":
    import requests
    import datetime
    import shapely
    import json
    from stac_collection_search import search_collections_verbose

    url = "https://eod-catalog-svc-prod.astraea.earth/collections"
    headers = {
            "Content-Type": "application/geo+json"
        }
    response = requests.get(url)
    collection_list_json_dict = response.json()
    temporal_extent_start = datetime.datetime(2019, 1, 1)
    temporal_extent_end = datetime.datetime(2021, 1, 1)
    spatial_extent = shapely.geometry.box(50, 0, 51, 1)
    collection_list = search_collections_verbose(collection_list_json_dict, spatial_extent=spatial_extent,
                                         temporal_extent_start=temporal_extent_start,
                                         temporal_extent_end=temporal_extent_end)

    print(json.dumps(collection_list, indent=4))
    url ="https://paituli.csc.fi/geoserver/ogc/collections"
    response = requests.get(url)
    collection_list_json_dict = response.json()
    temporal_extent_start = datetime.datetime(2019, 1, 1)
    temporal_extent_end = datetime.datetime(2021, 1, 1)
    spatial_extent = shapely.geometry.box(50, 0, 51, 1)
    collection_list = search_collections_verbose(collection_list_json_dict, spatial_extent=spatial_extent,
                                         temporal_extent_start=temporal_extent_start,
                                         temporal_extent_end=temporal_extent_end)

    print(json.dumps(collection_list, indent=4))
