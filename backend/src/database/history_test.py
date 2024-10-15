import unittest
from uuid import UUID
from .history import make_json_friendly


class TestUuidToStr(unittest.TestCase):
    def test_str(self):
        id = "3d94f101-a072-4fe1-befa-97a05c15f895"
        uuid = make_json_friendly(UUID(id))
        self.assertEqual(uuid, id)

    def test_dict(self):
        id = "3d94f101-a072-4fe1-befa-97a05c15f895"
        obj = make_json_friendly({"id": UUID(id)})
        self.assertEqual(obj["id"], id)
