from typing import Optional, List, TypedDict, AnyStr
import datetime
import shapely


class TemporalExtent(TypedDict):
    start: Optional[datetime.datetime]
    end: Optional[datetime.datetime]


class CollectionInfo(TypedDict):
    id: AnyStr
    spatial_extent: shapely.geometry.MultiPolygon
    temporal_extent: TemporalExtent


def get_shapely_object_from_bbox_list(bbox_list: List) -> shapely.geometry.Polygon:
    bbox_list_shapely = shapely.geometry.box(*bbox_list)
    return bbox_list_shapely


def get_collections(collection_list_json: dict) -> List[CollectionInfo]:
    collection_list: List[CollectionInfo] = []
    for i in collection_list_json["collections"]:
        collection_id = i["id"]
        spatial_extents = i["extent"]["spatial"]["bbox"]
        shapely_objects = [get_shapely_object_from_bbox_list(spatial_extent) for spatial_extent in spatial_extents]

        shapely_objects_multipolygon = shapely.geometry.MultiPolygon(shapely_objects)

        temporal_extent_start_string = i["extent"]["temporal"]["interval"][0][0]
        temporal_extent_end_string = i["extent"]["temporal"]["interval"][0][1]

        temporal_extent_start = _process_timestamp(
            temporal_extent_start_string) if temporal_extent_start_string else None
        temporal_extent_end = _process_timestamp(temporal_extent_end_string) if temporal_extent_end_string else None

        collection_info = CollectionInfo(
            id=collection_id,
            spatial_extent=shapely_objects_multipolygon,
            temporal_extent=TemporalExtent(
                start=temporal_extent_start,
                end=temporal_extent_end
            )
        )
        collection_list.append(collection_info)

    return collection_list


def _process_timestamp(timestamp: str) -> datetime:
    """
    Process a timestamp string into a datetime object.
    """
    potential_timestamp_formats = ['%Y-%m-%dT%H:%M:%S%Z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S.%f%z',
                                   '%Y-%m-%dT%H:%M:%S.%f']
    timestamp_datetime = None
    if timestamp is not None and timestamp != '..':
        for fmt in potential_timestamp_formats:
            try:
                timestamp_datetime = datetime.datetime.strptime(timestamp, fmt)
                break
            except ValueError:
                continue
        if timestamp_datetime is None:
            raise Exception
    return timestamp_datetime


if __name__ == "__main__":
    bbox_1 = [100, 0, 101, 1]
    bbox_2 = [102, 2, 103, 3]

    bbox_1_shapely = get_shapely_object_from_bbox_list(bbox_1)
    bbox_2_shapely = get_shapely_object_from_bbox_list(bbox_2)

    bbox_multipolygon = shapely.geometry.MultiPolygon([bbox_1_shapely, bbox_2_shapely])
