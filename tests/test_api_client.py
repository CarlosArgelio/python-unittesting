import unittest, requests
from unittest.mock import patch, Mock
from src.api_client import get_location


class ApiClientTest(unittest.TestCase):

    @patch("src.api_client.requests.get")
    def test_get_location_returns_expected_data(self, mock_get: Mock):
        ip = "8.8.8.8"

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "countryName": "United States of America",
            "regionName": "California",
            "cityName": "Mountain View",
        }
        data = get_location(ip)
        self.assertEqual(data.get("country"), "United States of America")

        mock_get.assert_called_once_with(f"https://freeipapi.com/api/json/{ip}")

    @patch("src.api_client.requests.get")
    def test_get_location_returns_side_effect(self, mock_get):
        mock_get.side_effect = [
            requests.exceptions.RequestException("Service Unavailable"),
            unittest.mock.Mock(
                status_code=200,
                json=lambda: {
                    "countryName": "USA",
                    "regionName": "FLORIDA",
                    "cityName": "MIAMI",
                },
            ),
        ]

        with self.assertRaises(requests.exceptions.RequestException):
            get_location("8.8.8.8")

        result = get_location("8.8.8.8")
        self.assertEqual(result.get("country"), "USA")
        self.assertEqual(result.get("region"), "FLORIDA")
        self.assertEqual(result.get("city"), "MIAMI")
