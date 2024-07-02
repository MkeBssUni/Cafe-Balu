import unittest
import json
from newPassword import app

mock_success = {
    "body": json.dumps({
        "username": "marianne",
        "temporary_password": "Aa123456.",
        "new_password": "Marianne1568481."
    })
}

class TestLogin(unittest.TestCase):
    def test_login_success(self):
        result = app.lambda_handler(mock_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
        body = json.loads(result["body"])