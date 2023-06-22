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
            spatial_extent=shapely.geometry.MultiPolygon(
                [
                    _get_shapely_object_from_bbox_list(spatial_extent)
                    for spatial_extent in i["extent"]["spatial"]["bbox"]
                ]
            ),
            temporal_extent=TemporalExtent(
                start=_process_timestamp(i["extent"]["temporal"]["interval"][0][0]),
                end=_process_timestamp(i["extent"]["temporal"]["interval"][-1][1]),
            ),
        )
        for i in collection_list_json["collections"]
    ]


def _process_timestamp(timestamp: str) -> datetime:
    """
    Process a timestamp string into a datetime object.
    """
    if timestamp is None:
        return None
    for fmt in [
        "%Y-%m-%dT%H:%M:%S%Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
    ]:
        try:
            return datetime.datetime.strptime(timestamp, fmt)
        except ValueError:
            continue
    raise ValueError(f"timestamp {timestamp} does not match any known formats")


def search_collections(
        collection_json_dict: dict,
        spatial_extent: shapely.geometry.Polygon = None,
        temporal_extent_start=None,
        temporal_extent_end=None,
) -> List[Dict[AnyStr, Any]]:
    collection_list = _get_collections(collection_json_dict)
    collections_spatially_filtered = []

    for collection in collection_list:
        try:
            if spatial_extent is None or spatial_extent.intersects(collection["spatial_extent"]):
                collections_spatially_filtered.append(collection)
        except shapely.errors.GEOSException:
            # make a bounding box around the collection["spatial_extent"] and check if it intersects with the spatial_extent
            # if it does, add it to the list
            print("Trying envelope")
            shapely_multipolygon = shapely.geometry.MultiPolygon(collection["spatial_extent"])
            shapely_multipolygon_bbox = shapely_multipolygon.envelope
            if spatial_extent.intersects(shapely_multipolygon_bbox):
                collections_spatially_filtered.append(collection)



    ids = []
    if temporal_extent_start is not None:
        temporal_extent_start = temporal_extent_start.replace(tzinfo=datetime.timezone.utc)
    if temporal_extent_end is not None:
        temporal_extent_end = temporal_extent_end.replace(tzinfo=datetime.timezone.utc)
    for collection in collections_spatially_filtered:
        collection_temporal_extent_start = collection["temporal_extent"]["start"]
        collection_temporal_extent_end = collection["temporal_extent"]["end"]
        if collection_temporal_extent_start is not None:
            collection_temporal_extent_start_utc = collection_temporal_extent_start.replace(
                tzinfo=datetime.timezone.utc)
        else:
            collection_temporal_extent_start_utc = None
        if collection_temporal_extent_end is not None:
            collection_temporal_extent_end_utc = collection_temporal_extent_end.replace(tzinfo=datetime.timezone.utc)
        else:
            collection_temporal_extent_end_utc = None

        if (
                temporal_extent_start is None
                or collection_temporal_extent_end_utc is None
                or collection_temporal_extent_end_utc >= temporal_extent_start
        ) and (
                temporal_extent_end is None
                or collection_temporal_extent_start_utc is None
                or collection_temporal_extent_start_utc <= temporal_extent_end
        ):
            ids.append(collection["id"])
    return ids


def search_collections_verbose(
        collection_json_dict: dict,
        spatial_extent: shapely.geometry.Polygon = None,
        temporal_extent_start=None,
        temporal_extent_end=None,
) -> List[AnyStr]:
    ids = search_collections(collection_json_dict=collection_json_dict,
                             spatial_extent=spatial_extent,
                             temporal_extent_start=temporal_extent_start,
                             temporal_extent_end=temporal_extent_end)
    # filter the collection_json_dict to only include the collections that are in the ids list
    return [
        collection
        for collection in collection_json_dict["collections"]
        if collection["id"] in ids
    ]