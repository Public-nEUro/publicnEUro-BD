import unittest
from .passkey import hash_passkey, check_passkey


class TestPasskey(unittest.TestCase):
    def test_passkey(self):
        hash = hash_passkey("right_passkey")
        self.assertEqual(len(hash), 64)
        self.assertTrue(check_passkey("right_passkey", hash))
        self.assertFalse(check_passkey("wrong_passkey", hash))
