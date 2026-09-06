"""
Frontend Integration Test for GENESIS Cinema Character Studio & Stage Summon
-----------------------------------------------------------------------------
Tests:
- Serves index.html with modal-character-studio and stage-actor-layer
- Serves character_studio_ui.js
- Verifies DOM element IDs and integration points
"""

import os
import sys
import time
import threading
import urllib.request
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "GENESIS_CINEMA_STUDIO"))

import server


class TestFrontendCharacterStudio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8098
        server.PORT = cls.port
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

    def test_01_index_html_contains_character_studio(self):
        url = f"http://localhost:{self.port}/index.html"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            html = resp.read().decode("utf-8")
            
            # Check modal
            self.assertIn('id="modal-character-studio"', html)
            self.assertIn('id="tab-char-prompt"', html)
            self.assertIn('id="tab-char-photos"', html)
            self.assertIn('id="dropzone-front"', html)
            self.assertIn('id="dropzone-costume-ec"', html)
            self.assertIn('id="preview-matte-front"', html)
            self.assertIn('id="slider-defringe-strength"', html)

            # Check stage actor overlay
            self.assertIn('id="stage-actor-layer"', html)
            self.assertIn('id="stage-actor-entity"', html)
            self.assertIn('id="stage-actor-shadow"', html)
            self.assertIn('id="btn-summon-stage-actor"', html)

            # Check script tag
            self.assertIn('src="character_studio_ui.js"', html)

    def test_02_serves_character_studio_ui_js(self):
        url = f"http://localhost:{self.port}/character_studio_ui.js"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            js = resp.read().decode("utf-8")
            self.assertIn("CharacterStudioUI", js)
            self.assertIn("toggleStageActor", js)
            self.assertIn("executeCharacterGeneration", js)
            self.assertIn("handleCostumeDrop", js)


if __name__ == "__main__":
    unittest.main()
