import unittest
import json
from login import app

mock_success = {
    "body": json.dumps({
        "username": "balu",
        "password": "Admin123."
    })
}

mock_wrong_password = {
    "body": json.dumps({
        "username": "balu",
        "password": "oasindoasidnsd"
    })
}

mock_invalid_json = {
    "body": json.dumps({
        "property": "anything"
    })
}

class TestLogin(unittest.TestCase):
    def test_login_success(self):
        result = app.lambda_handler(mock_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
    def test_login_wrong_password(self):
        result = app.lambda_handler(mock_wrong_password, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
    def test_login_invalid_password(self):
        result = app.lambda_handler(mock_invalid_json, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 500)
