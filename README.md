# STAC Collection Search
Quick utility which enables you to search for STAC collections with a given bbox and datetime extent.

## How to use

``` python
  import requests
  import datetime
  import shapely
  from stac_collection_search import search_collections

  url ="https://planetarycomputer.microsoft.com/api/stac/v1/collections"
  response = requests.get(url)
  collection_list_json_dict = response.json()
  temporal_extent_start = datetime.datetime(2019, 1, 1)
  temporal_extent_end = datetime.datetime(2021, 1, 1)
  spatial_extent = shapely.geometry.box(50, 0, 51, 1)
  collection_list = search_collections(collection_list_json_dict, spatial_extent=spatial_extent,
                                      temporal_extent_start=temporal_extent_start,
                                      temporal_extent_end=temporal_extent_end)
  print(collection_list, len(collection_list)) """ -> ['3dep-seamless', 'sentinel-1-rtc', '...'], 66 """

```