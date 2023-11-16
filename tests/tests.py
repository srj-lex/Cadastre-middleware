import unittest
import requests


class TestCadastreService(unittest.TestCase):
    URL = "http://cadastre_server:5000"

    def test_1_get_ping(self):
        response = requests.get(self.URL + "/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "online")
        print("Test 1 completed")

    def test_2_get_query_without_params(self):
        payload = {}
        response = requests.get(self.URL + "/query", params=payload)
        self.assertEqual(response.status_code, 400)
        print("Test 2 completed")

    def test_3_get_query_with_invalid_params(self):
        payload = {
            "volume": 45,
            "length": 10,
            "width": 15
        }
        response = requests.get(self.URL + "/query", params=payload)
        self.assertEqual(response.status_code, 400)
        print("Test 3 completed")

    def test_4_get_query_with_valid_params(self):
        payload = {
            "cadastre_number": 123,
            "longitude": 45.1,
            "latitude": 48.6
        }
        response = requests.get(self.URL + "/query", params=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        print("Test 4 completed")

    def test_5_get_result_without_param(self):
        payload = {}
        response = requests.get(self.URL + "/result", params=payload)
        self.assertEqual(response.status_code, 400)
        print("Test 5 completed")

    def test_6_get_result_with_invalid_param(self):
        payload = {
            "id": "alng7464ag"
        }
        response = requests.get(self.URL + "/result", params=payload)
        self.assertEqual(response.status_code, 400)
        print("Test 6 completed")

    def test_7_get_history_without_param(self):
        payload = {}
        response = requests.get(self.URL + "/history", params=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        print("Test 7 completed")

    def test_8_get_hisory_with_invalid_param(self):
        payload = {
            "cadastre_number": "a7464ag"
        }
        response = requests.get(self.URL + "/history", params=payload)
        self.assertEqual(response.status_code, 400)
        print("Test 8 completed")

    def test_9_get_history_with_not_exists_number(self):
        payload = {
            "cadastre_number": 5481
        }
        response = requests.get(self.URL + "/history", params=payload)
        self.assertEqual(response.status_code, 404)
        print("Test 9 completed")

    def test_10_get_history_with_valid_param(self):
        payload = {
            "cadastre_number": 123
        }
        response = requests.get(self.URL + "/history", params=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        print("Test 10 completed")


def suite():
    test_suite = unittest.TestSuite()
    tests = [
        TestCadastreService('test_1_get_ping'),
        TestCadastreService('test_2_get_query_without_params'),
        TestCadastreService('test_3_get_query_with_invalid_params'),
        TestCadastreService('test_4_get_query_with_valid_params'),
        TestCadastreService('test_5_get_result_without_param'),
        TestCadastreService('test_6_get_result_with_invalid_param'),
        TestCadastreService('test_7_get_history_without_param'),
        TestCadastreService('test_8_get_hisory_with_invalid_param'),
        TestCadastreService('test_9_get_history_with_not_exists_number'),
        TestCadastreService('test_10_get_history_with_valid_param'),
    ]
    test_suite.addTests(tests)
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
