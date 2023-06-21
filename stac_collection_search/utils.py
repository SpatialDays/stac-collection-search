import datetime
from typing import Optional, List, TypedDict, AnyStr, Dict, Any

import shapely.geometry


class TemporalExtent(TypedDict):
    start: Optional[datetime.datetime]
    end: Optional[datetime.datetime]


class CollectionInfo(TypedDict):
    id: AnyStr
    spatial_extent: shapely.geometry.MultiPolygon
    temporal_extent: TemporalExtent


def _get_shapely_object_from_bbox_list(bbox_list: List) -> shapely.geometry.Polygon:
    return shapely.geometry.box(*bbox_list)


def _get_collections(collection_list_json: dict) -> List[CollectionInfo]:
    return [
        CollectionInfo(
            id=i["id"],
            spatial_extent=shapely.geometry.MultiPolygon([
                _get_shapely_object_from_bbox_list(spatial_extent)
                for spatial_extent in i["extent"]["spatial"]["bbox"]
            ]),
            temporal_extent=TemporalExtent(
                start=_process_timestamp(i["extent"]["temporal"]["interval"][0][0]),
                end=_process_timestamp(i["extent"]["temporal"]["interval"][0][1])
            )
        ) for i in collection_list_json["collections"]
    ]


def _process_timestamp(timestamp: str) -> datetime:
    """
    Process a timestamp string into a datetime object.
    """
    if timestamp is None:
        return None
    for fmt in ['%Y-%m-%dT%H:%M:%S%Z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M:%S.%f']:
        try:
            return datetime.datetime.strptime(timestamp, fmt)
        except ValueError:
            continue
    raise ValueError(f"timestamp {timestamp} does not match any known formats")


def search_collections(collection_json_dict: dict, spatial_extent: shapely.geometry.Polygon = None,
                       temporal_extent_start=None, temporal_extent_end=None) -> List[Dict[AnyStr, Any]]:
    # Ensure that temporal_extent_start and temporal_extent_end are timezone-aware (in UTC)
    if temporal_extent_start and temporal_extent_start.tzinfo is None:
        temporal_extent_start = temporal_extent_start.replace(tzinfo=datetime.timezone.utc)
    if temporal_extent_end and temporal_extent_end.tzinfo is None:
        temporal_extent_end = temporal_extent_end.replace(tzinfo=datetime.timezone.utc)

    collection_list = _get_collections(collection_json_dict)

    # First, we filter by spatial extent
    collections_spatially_filtered = (
        [collection for collection in collection_list if spatial_extent.intersects(collection["spatial_extent"])]
        if spatial_extent else collection_list
    )

    # Now we apply time-based filter on spatially filtered collections
    return [
        collection["id"] for collection in collections_spatially_filtered
        if (temporal_extent_start is None or collection["temporal_extent"]["end"] is None or
            collection["temporal_extent"]["end"] >= temporal_extent_start) and
           (temporal_extent_end is None or collection["temporal_extent"]["start"] is None or
            collection["temporal_extent"]["start"] <= temporal_extent_end)
    ]
