import json
import unittest
from newPassword import app
from unittest.mock import patch
from botocore.exceptions import ClientError

mock_success = {
    "body": json.dumps({
        "username": "miguel",
        "current_password": "Miguel123.",
        "new_password": "Miguel1234."
    })
}

mock_missing_params = {
    "body": json.dumps({
        "username": "miguel",
        "current_password": "Miguel1234."
    })
}

class TestResetPassword(unittest.TestCase):
    @patch("newPassword.app.boto3.client")
    def test_new_password_success(self, mock_boto_client):
        mock_client_instance = mock_boto_client.return_value
        mock_client_instance.admin_initiate_auth.return_value = {
            "ChallengeName": "NEW_PASSWORD_REQUIRED",
            "Session": "session"
        }
        result = app.lambda_handler(mock_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
        self.assertIn("Password changed successfully", result["body"])

    @patch("newPassword.app.boto3.client")
    def test_password_update_success(self, mock_boto_client):
        mock_client_instance = mock_boto_client.return_value
        mock_client_instance.admin_initiate_auth.return_value = {
            "AuthenticationResult": {
                "AccessToken": "access_token"
            }
        }
        result = app.lambda_handler(mock_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 200)
        self.assertIn("Password updated successfully", result["body"])

    @patch("newPassword.app.boto3.client")
    def test_unexpected_challenge(self, mock_boto_client):
        mock_client_instance = mock_boto_client.return_value
        mock_client_instance.admin_initiate_auth.return_value = {
            "ChallengeName": "UNEXPECTED_CHALLENGE",
            "Session": "session"
        }
        result = app.lambda_handler(mock_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        self.assertIn("Unexpected response during authentication", result["body"])

    @patch("newPassword.app.boto3.client")
    def test_client_error(self, mock_boto_client):
        mock_client_instance = mock_boto_client.return_value
        error_response = {
            'Error': {
                'Code': 'InvalidParameterException',
                'Message': 'An error occurred'
            }
        }

        mock_client_instance.admin_initiate_auth.side_effect = ClientError(error_response, 'admin_initiate_auth')

        result = app.lambda_handler(mock_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 400)
        self.assertIn("An error occurred", result["body"])

    @patch("newPassword.app.boto3.client")
    def test_error_500(self, mock_boto_client):
        mock_client_instance = mock_boto_client.return_value
        error_response = {
            'Error': {
                'Code': 'InvalidParameterException',
                'Message': 'An error occurred'
            }
        }

        mock_client_instance.admin_initiate_auth.side_effect = Exception(error_response)

        result = app.lambda_handler(mock_success, None)
        status_code = result["statusCode"]
        self.assertEqual(status_code, 500)
        self.assertIn("InvalidParameterException", result["body"])
