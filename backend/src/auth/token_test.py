import unittest
import jwt
from .token import create_token_from_client_secret, get_verified_payload_from_token


class TestToken(unittest.TestCase):
    def test_token(self):
        token = create_token_from_client_secret("id123", "secret123")
        payload = get_verified_payload_from_token(token, "secret123")
        self.assertEqual(payload["sub"], "id123")
        with self.assertRaises(jwt.InvalidTokenError):
            get_verified_payload_from_token(token, "secret124")
