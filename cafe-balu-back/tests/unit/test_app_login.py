import unittest
import json
from login import app
from unittest.mock import patch, MagicMock

mock_success = {
    "body": json.dumps({
        "username": "marianne",
        "password": "Marianne1568481."
    })
}

class TestLogin(unittest.TestCase):
    def test_login_success(self):
        result = app.lambda_handler(mock_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
        body = json.loads(result["body"])