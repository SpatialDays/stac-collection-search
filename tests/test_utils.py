import json
import unittest

import shapely
import datetime
from stac_collection_search import *


class TestSearchCollections(unittest.TestCase):

    def setUp(self) -> None:
        self.collection_list_json_dict = json.loads("""{
                    "collections": [
                        {
                            "id": "landsat-8",
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
                                            "2020-01-01T00:00:00Z",
                                            "2021-01-01T00:00:00Z"
                                        ]
                                    ]
                                }
                            }
                        },
                                        {
                            "id": "landsat-7",
                            "extent": {
                                "spatial": {
                                    "bbox": [
                                        [
                                            60,
                                            10,
                                            61,
                                            11
                                        ]
                                    ]
                                },
                                "temporal": {
                                    "interval": [
                                        [
                                            "2015-01-01T00:00:00Z",
                                            "2016-01-01T00:00:00Z"
                                        ]
                                    ]
                                }
                            }
                        }

                    ]
                }
                """)

    def test_search_collections_only_spatial_extent_bbox(self):
        bbox_shapely = shapely.geometry.box(50, 0, 51, 1)
        collection_list = search_collections(self.collection_list_json_dict, spatial_extent=bbox_shapely)
        self.assertEqual(len(collection_list), 1)
        self.assertEqual(collection_list[0], "landsat-8")
        bbox_shapely = shapely.geometry.box(60, 10, 61, 11)
        collection_list = search_collections(self.collection_list_json_dict, spatial_extent=bbox_shapely)
        self.assertEqual(len(collection_list), 1)
        self.assertEqual(collection_list[0], "landsat-7")
        bbox_shapely = shapely.geometry.box(50, 0, 61, 11)
        collection_list = search_collections(self.collection_list_json_dict, spatial_extent=bbox_shapely)
        self.assertEqual(len(collection_list), 2)
        self.assertEqual(collection_list[0], "landsat-8")
        self.assertEqual(collection_list[1], "landsat-7")

    def test_search_collections_only_temporal_extent_collection_fully_contained(self):
        start_date = datetime.datetime(2019, 1, 1)
        end_date = datetime.datetime(2022, 1, 1)
        collection_list = search_collections(self.collection_list_json_dict, temporal_extent_start=start_date,
                                             temporal_extent_end=end_date)
        self.assertEqual(len(collection_list), 1)
        self.assertEqual(collection_list[0], "landsat-8")

    def test_search_collections_only_temporal_extent_collection_within(self):
        start_date = datetime.datetime(2020, 5, 5)
        end_date = datetime.datetime(2020, 6, 5)
        collection_list = search_collections(self.collection_list_json_dict, temporal_extent_start=start_date,
                                             temporal_extent_end=end_date)
        self.assertEqual(len(collection_list), 1)
        self.assertEqual(collection_list[0], "landsat-8")

    def test_search_collections_only_temporal_extent_collection_overlaps_start(self):
        start_date = datetime.datetime(2019, 1, 1)
        end_date = datetime.datetime(2020, 6, 5)
        collection_list = search_collections(self.collection_list_json_dict, temporal_extent_start=start_date,
                                             temporal_extent_end=end_date)
        self.assertEqual(len(collection_list), 1)
        self.assertEqual(collection_list[0], "landsat-8")

    def test_search_collections_only_temporal_extent_collection_overlaps_end(self):
        start_date = datetime.datetime(2020, 6, 5)
        end_date = datetime.datetime(2022, 1, 1)
        collection_list = search_collections(self.collection_list_json_dict, temporal_extent_start=start_date,
                                             temporal_extent_end=end_date)
        self.assertEqual(len(collection_list), 1)
        self.assertEqual(collection_list[0], "landsat-8")

    def test_search_collections_only_temporal_extent_collection_fully_contained_multiple_collections(self):
        start_date = datetime.datetime(2010, 1, 1)
        end_date = datetime.datetime(2022, 1, 1)
        collection_list = search_collections(self.collection_list_json_dict, temporal_extent_start=start_date,
                                             temporal_extent_end=end_date)
        self.assertEqual(len(collection_list), 2)
        self.assertEqual(collection_list[0], "landsat-8")
        self.assertEqual(collection_list[1], "landsat-7")

    def test_search_collections_with_spatial_and_temporal_extent_collection_fully_contained_multiple_collections(self):
        start_date = datetime.datetime(2010, 1, 1)
        end_date = datetime.datetime(2022, 1, 1)
        bbox_shapely = shapely.geometry.box(50, 0, 61, 11)
        collection_list = search_collections(self.collection_list_json_dict, spatial_extent=bbox_shapely,
                                             temporal_extent_start=start_date,
                                             temporal_extent_end=end_date)
        self.assertEqual(len(collection_list), 2)
        self.assertEqual(collection_list[0], "landsat-8")
        self.assertEqual(collection_list[1], "landsat-7")

        start_date = datetime.datetime(2010, 1, 1)
        end_date = datetime.datetime(2022, 1, 1)
        bbox_shapely = shapely.geometry.box(50, 0, 51, 1)
        collection_list = search_collections(self.collection_list_json_dict, spatial_extent=bbox_shapely,
                                             temporal_extent_start=start_date,
                                             temporal_extent_end=end_date)
        self.assertEqual(len(collection_list), 1)
        self.assertEqual(collection_list[0], "landsat-8")

        start_date = datetime.datetime(2010, 1, 1)
        end_date = datetime.datetime(2022, 1, 1)
        bbox_shapely = shapely.geometry.box(60, 10, 61, 11)
        collection_list = search_collections(self.collection_list_json_dict, spatial_extent=bbox_shapely,
                                             temporal_extent_start=start_date,
                                             temporal_extent_end=end_date)
        self.assertEqual(len(collection_list), 1)
        self.assertEqual(collection_list[0], "landsat-7")
