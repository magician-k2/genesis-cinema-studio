import unittest
import json
import urllib.request
import urllib.parse

class TestAlleywayScoutAPI(unittest.TestCase):
    def test_01_global_preset_cities(self):
        """Verify global alleyway database matches Paris, London, Rome, Kyoto, Hong Kong."""
        cities = ["パリ", "ロンドン", "ローマ", "京都", "香港", "ニューヨーク"]
        for city in cities:
            url = f"http://localhost:8080/api/scout/alleyway?query={urllib.parse.quote(city)}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode('utf-8'))
                self.assertTrue(data.get("success"))
                self.assertTrue(data.get("isAlleyway"))
                self.assertIsNotNone(data.get("lat"))
                self.assertIsNotNone(data.get("lng"))
                self.assertIn("🏮", data.get("locationName"))
                self.assertIn("cinemaTag", data)

    def test_02_dynamic_coordinates_alleyway(self):
        """Verify dynamic alleyway query with arbitrary coords."""
        query_enc = urllib.parse.quote("尾道")
        url = f"http://localhost:8080/api/scout/alleyway?query={query_enc}&lat=34.4089&lng=133.1956"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=8) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get("success"))
            self.assertTrue(data.get("isAlleyway"))

if __name__ == '__main__':
    unittest.main()
