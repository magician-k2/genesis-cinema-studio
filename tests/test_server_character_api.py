"""
End-to-End API Test for Server Character Matting & Vault Endpoints
------------------------------------------------------------------
Tests:
- POST /api/character/process_sheet (Input A)
- POST /api/character/process_photos (Input B)
- GET /api/characters
- GET /api/characters/<id>
- GET /characters/<id>/front.png (Static file serving)
"""

import os
import sys
import json
import base64
import io
import time
import threading
import urllib.request
import unittest
from PIL import Image, ImageDraw

# Add roots to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "GENESIS_CINEMA_STUDIO"))

import server


def image_to_base64_data_uri(img: Image.Image) -> str:
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64_str}"


class TestServerCharacterAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8099
        server.PORT = cls.port
        # Create socket server on 8099
        import socketserver
        socketserver.TCPServer.allow_reuse_address = True
        cls.httpd = socketserver.TCPServer(("", cls.port), server.GenesisCinemaHandler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.httpd.shutdown()
            cls.httpd.server_close()
        except Exception:
            pass

    def _create_mock_sheet(self, w=1200, h=600):
        img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        col_w = w // 4
        for i in range(4):
            cx = i * col_w + col_w // 2
            draw.ellipse([cx - 30, 80, cx + 30, 140], fill=(230, 190, 160, 255))
            draw.rectangle([cx - 40, 140, cx + 40, 450], fill=(30, 40, 60, 255))
            draw.rectangle([cx - 30, 450, cx + 30, 550], fill=(10, 10, 10, 255))
        return img

    def test_01_api_process_sheet(self):
        sheet_img = self._create_mock_sheet()
        data_uri = image_to_base64_data_uri(sheet_img)

        payload = {
            "char_id": "test_ren_e2e",
            "sheet_image": data_uri,
            "metadata": {
                "name": "如月 蓮 (E2E)",
                "name_en": "Ren Kisaragi E2E",
                "age": 26,
                "gender": "male",
                "height_m": 1.80,
                "costume_tags": ["ロングトレンチコート"]
            }
        }

        req = urllib.request.Request(
            f"http://localhost:{self.port}/api/character/process_sheet",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            self.assertEqual(resp.status, 200)
            res = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(res["success"])
            self.assertEqual(res["character"]["id"], "test_ren_e2e")
            self.assertIn("front", res["character"]["views"])

    def test_02_api_process_photos(self):
        # Create 4 mock photos
        photos = {}
        for view in ["front", "right", "back", "left"]:
            img = Image.new("RGBA", (300, 500), (255, 255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.rectangle([80, 50, 220, 450], fill=(200, 80, 140, 255))
            photos[view] = image_to_base64_data_uri(img)

        payload = {
            "char_id": "test_idol_e2e",
            "photos": photos,
            "metadata": {
                "name": "星野 まゆ (E2E)",
                "name_en": "Mayu Hoshino E2E",
                "age": 18,
                "gender": "female",
                "height_m": 1.56,
                "costume_tags": ["ライブ衣装", "リボン"]
            }
        }

        req = urllib.request.Request(
            f"http://localhost:{self.port}/api/character/process_photos",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            self.assertEqual(resp.status, 200)
            res = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(res["success"])
            self.assertEqual(res["character"]["id"], "test_idol_e2e")
            self.assertEqual(res["character"]["height_m"], 1.56)

    def test_03_api_get_characters_list(self):
        req = urllib.request.Request(f"http://localhost:{self.port}/api/characters")
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            chars = json.loads(resp.read().decode("utf-8"))
            self.assertIsInstance(chars, list)
            ids = [c["id"] for c in chars]
            self.assertIn("test_ren_e2e", ids)
            self.assertIn("test_idol_e2e", ids)

    def test_04_api_get_single_character(self):
        req = urllib.request.Request(f"http://localhost:{self.port}/api/characters/test_ren_e2e")
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            char = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(char["id"], "test_ren_e2e")
            self.assertEqual(char["name"], "如月 蓮 (E2E)")
            self.assertIn("front", char["views"])

    def test_05_static_png_serving(self):
        # Test downloading the transparent front.png via static server
        url = f"http://localhost:{self.port}/characters/test_ren_e2e/front.png"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            content_type = resp.headers.get("Content-Type")
            self.assertIn("image/png", content_type)
            png_bytes = resp.read()
            img = Image.open(io.BytesIO(png_bytes))
            self.assertEqual(img.mode, "RGBA")
            self.assertEqual(img.size, (600, 1000))


if __name__ == "__main__":
    unittest.main()
