import unittest
from .password import gen_hash_and_salt, check_password


class TestPassword(unittest.TestCase):
    def test_password(self):
        hash, salt = gen_hash_and_salt("right_password")
        self.assertTrue(check_password("right_password", hash, salt))
        self.assertFalse(check_password("wrong_password", hash, salt))
