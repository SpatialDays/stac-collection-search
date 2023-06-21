import unittest
import shapely
import json
from stac_collection_search import *


class TestGetShapelyObjectFromBboxList(unittest.TestCase):
    def test_get_shapely_object_from_bbox_list(self):
        bbox_list = [-180, -90, 180, 90]
        bbox_list_shapely = get_shapely_object_from_bbox_list(bbox_list)
        self.assertEqual(
            bbox_list_shapely.bounds, (-180.0, -90.0, 180.0, 90.0)
        )


class TestGetCollectionsFromCollectionJson(unittest.TestCase):

    def test_get_collections_from_collection_json(self):
        collection_list_json_dict =  json.loads("""{
            "collections": [
                {
                    "id": "landsat-8-l1",
                    "extent": {
                        "spatial": {
                            "bbox": [
                                [
                                    50,
                                    0,
                                    51,
                                    1
                                ]
                            ]
                        },
                        "temporal": {
                            "interval": [
                                [
                                    "2013-04-11T00:00:00Z",
                                    "2013-04-12T00:00:00Z"
                                ]
                            ]
                        }
                    }
                }
            ]
        }
        """)
        collection_list = get_collections(collection_list_json_dict)
        self.assertEqual(collection_list[0]["id"], "landsat-8-l1")
        self.assertEqual(collection_list[0]["spatial_extent"].bounds, (50.0, 0.0, 51.0, 1.0))
        self.assertEqual(collection_list[0]["temporal_extent"]["start"].year, 2013)
        self.assertEqual(collection_list[0]["temporal_extent"]["start"].month, 4)
        self.assertEqual(collection_list[0]["temporal_extent"]["start"].day, 11)
        self.assertEqual(collection_list[0]["temporal_extent"]["end"].year, 2013)
        self.assertEqual(collection_list[0]["temporal_extent"]["end"].month, 4)
        self.assertEqual(collection_list[0]["temporal_extent"]["end"].day, 12)

    def test_get_collections_from_collection_json_multiple_bboxes(self):
        collection_list_json_dict =  json.loads("""{
            "collections": [
                {
                    "id": "landsat-8-l1",
                    "extent": {
                        "spatial": {
                            "bbox": [
                                [
                                    50,
                                    0,
                                    51,
                                    1
                                ],
                                [   
                                    60,
                                    0,
                                    61,
                                    1
                                ]
                            ]
                        },
                        "temporal": {
                            "interval": [
                                [
                                    "2013-04-11T00:00:00Z",
                                    "2013-04-12T00:00:00Z"
                                ]
                            ]
                        }
                    }
                }
            ]
        }
        """)
        collection_list = get_collections(collection_list_json_dict)
        self.assertEqual(collection_list[0]["id"], "landsat-8-l1")
        self.assertEqual(collection_list[0]["spatial_extent"].bounds, (50.0, 0.0, 61.0, 1.0))
        self.assertEqual(collection_list[0]["temporal_extent"]["start"].year, 2013)
        self.assertEqual(collection_list[0]["temporal_extent"]["start"].month, 4)
        self.assertEqual(collection_list[0]["temporal_extent"]["start"].day, 11)
        self.assertEqual(collection_list[0]["temporal_extent"]["end"].year, 2013)
        self.assertEqual(collection_list[0]["temporal_extent"]["end"].month, 4)
        self.assertEqual(collection_list[0]["temporal_extent"]["end"].day, 12)

    def test_get_collections_from_collection_json_no_end_timestamp(self):
        collection_list_json_dict =  json.loads("""{
            "collections": [
                {
                    "id": "landsat-8-l1",
                    "extent": {
                        "spatial": {
                            "bbox": [
                                [
                                    50,
                                    0,
                                    51,
                                    1
                                ]
                            ]
                        },
                        "temporal": {
                            "interval": [
                                [
                                    "2013-04-11T00:00:00Z",
                                    null
                                ]
                            ]
                        }
                    }
                }
            ]
        }
        """)
        collection_list = get_collections(collection_list_json_dict)
        self.assertEqual(collection_list[0]["id"], "landsat-8-l1")
        self.assertEqual(collection_list[0]["spatial_extent"].bounds, (50.0, 0.0, 51.0, 1.0))
        self.assertEqual(collection_list[0]["temporal_extent"]["start"].year, 2013)
        self.assertEqual(collection_list[0]["temporal_extent"]["start"].month, 4)
        self.assertEqual(collection_list[0]["temporal_extent"]["start"].day, 11)
        self.assertEqual(collection_list[0]["temporal_extent"]["end"], None)

    def test_get_collections_from_collection_json_no_start_timestamp(self):
        collection_list_json_dict =  json.loads("""{
            "collections": [
                {
                    "id": "landsat-8-l1",
                    "extent": {
                        "spatial": {
                            "bbox": [
                                [
                                    50,
                                    0,
                                    51,
                                    1
                                ]
                            ]
                        },
                        "temporal": {
                            "interval": [
                                [
                                    null,
                                    "2013-04-12T00:00:00Z"
                                ]
                            ]
                        }
                    }
                }
            ]
        }
        """)
        collection_list = get_collections(collection_list_json_dict)
        self.assertEqual(collection_list[0]["id"], "landsat-8-l1")
        self.assertEqual(collection_list[0]["spatial_extent"].bounds, (50.0, 0.0, 51.0, 1.0))
        self.assertEqual(collection_list[0]["temporal_extent"]["start"], None)
        self.assertEqual(collection_list[0]["temporal_extent"]["end"].year, 2013)
        self.assertEqual(collection_list[0]["temporal_extent"]["end"].month, 4)
        self.assertEqual(collection_list[0]["temporal_extent"]["end"].day, 12)