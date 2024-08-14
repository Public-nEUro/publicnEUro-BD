import unittest
from .password import gen_hash_and_salt, check_password, hash_passkey, check_passkey


class TestPassword(unittest.TestCase):
    def test_password(self):
        hash, salt = gen_hash_and_salt("right_password")
        self.assertEqual(len(hash), 64)
        self.assertEqual(len(salt), 32)
        self.assertTrue(check_password("right_password", hash, salt))
        self.assertFalse(check_password("wrong_password", hash, salt))

    def test_passkey(self):
        hash = hash_passkey("right_passkey")
        self.assertEqual(len(hash), 64)
        self.assertTrue(check_passkey("right_passkey", hash))
        self.assertFalse(check_passkey("wrong_passkey", hash))
