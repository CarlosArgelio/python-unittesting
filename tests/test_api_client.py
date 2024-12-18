import unittest
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
