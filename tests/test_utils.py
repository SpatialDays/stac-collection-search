import unittest
import shapely
from stac_collection_search import *


class TestGetShapelyObjectFromBboxList(unittest.TestCase):
    def tes_get_shapely_object_from_bbox_list(self):
        bbox_list = [-180, -90, 180, 90]
        bbox_list_shapely = get_shapely_object_from_bbox_list(bbox_list)
        self.assertEqual(type(bbox_list_shapely), shapely.geometry.box)
        self.assertEqual(
            bbox_list_shapely.bounds, (-180.0, -90.0, 180.0, 90.0)
        )
