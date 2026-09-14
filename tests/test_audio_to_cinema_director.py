# -*- coding: utf-8 -*-
"""
🧪 Test Suite: Audio-to-Cinema Synchronized Video Director Engine
================================================================
"""

import sys
import json
import urllib.request
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.genesis_audio_to_cinema_director import (
    analyze_timbre_to_cinematic_look,
    decompose_song_structure,
    generate_synchronized_cinema_storyboard,
)

class TestAudioToCinemaDirector(unittest.TestCase):

    def test_timbre_to_cinematic_look_cyberpunk(self):
        feat = {
            "bpm": 130.0,
            "key": "D Minor",
            "spectral_centroid": 1700.0,
            "spectral_flatness": 0.025,
            "percussive_ratio": 0.6,
            "sub_bass_ratio": 0.45
        }
        look = analyze_timbre_to_cinematic_look(feat)
        self.assertIn("ARRI Master Anamorphic", look["lens_choice"])
        self.assertIn("Kodak 2383", look["lut_preset"])
        self.assertIn("Chiaroscuro", look["lighting_setup"])
        self.assertNotIn("Kinetic Fast-Cut", look["cinematic_rhythm"])

    def test_timbre_to_cinematic_look_bright(self):
        feat = {
            "bpm": 140.0,
            "key": "G Major",
            "spectral_centroid": 3400.0,
            "spectral_flatness": 0.005,
            "percussive_ratio": 0.3,
            "sub_bass_ratio": 0.2
        }
        look = analyze_timbre_to_cinematic_look(feat)
        self.assertIn("Cooke S4/i", look["lens_choice"])
        self.assertIn("Fuji ETERNA", look["lut_preset"])
        self.assertIn("Kinetic Fast-Cut", look["cinematic_rhythm"])

    def test_decompose_song_structure(self):
        total_dur = 60.0
        feat = {"bpm": 128.0, "key": "A Minor"}
        sections = decompose_song_structure(feat, total_duration_sec=total_dur)

        self.assertEqual(len(sections), 5)
        self.assertEqual(sections[0]["section"], "Intro")
        self.assertEqual(sections[1]["section"], "Verse 1")
        self.assertEqual(sections[2]["section"], "Build-up (Rise)")
        self.assertEqual(sections[3]["section"], "Chorus / Drop")
        self.assertEqual(sections[4]["section"], "Outro")

        self.assertEqual(sections[0]["start_sec"], 0.0)
        self.assertEqual(sections[-1]["end_sec"], total_dur)
        for i in range(len(sections) - 1):
            self.assertLess(abs(sections[i]["end_sec"] - sections[i+1]["start_sec"]), 0.01)

        self.assertLess(sections[0]["energy_level"], sections[1]["energy_level"])
        self.assertLess(sections[1]["energy_level"], sections[2]["energy_level"])
        self.assertLess(sections[2]["energy_level"], sections[3]["energy_level"])
        self.assertEqual(sections[3]["energy_level"], 100)
        self.assertLess(sections[4]["energy_level"], sections[3]["energy_level"])

    def test_generate_synchronized_cinema_storyboard(self):
        feat = {
            "bpm": 124.0,
            "key": "C Minor",
            "spectral_centroid": 2400.0,
            "spectral_flatness": 0.012,
            "percussive_ratio": 0.42,
            "sub_bass_ratio": 0.38
        }
        res = generate_synchronized_cinema_storyboard(
            features=feat,
            track_title="Neo Tokyo Nightfall",
            scene_context="雨の路地裏 潜入作戦",
            total_duration_sec=60.0
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["track_title"], "Neo Tokyo Nightfall")
        self.assertEqual(len(res["storyboard_cuts"]), 5)
        for cut in res["storyboard_cuts"]:
            self.assertIn("CUT_", cut["cut_id"])
            self.assertGreater(len(cut["video_generation_prompt"]), 50)
            self.assertIn("Cinematic 35mm film still", cut["video_generation_prompt"])

    def test_api_endpoint_integration(self):
        url = "http://localhost:8080/api/music/to_cinema_storyboard"
        payload = {
            "features": {
                "bpm": 128.0,
                "key": "A Minor",
                "spectral_centroid": 2900.0,
                "spectral_flatness": 0.015,
                "percussive_ratio": 0.5,
                "sub_bass_ratio": 0.35
            },
            "track_title": "Tokyo Midnight Drive",
            "scene_context": "ネオ新宿首都高チェイス",
            "total_duration_sec": 60.0
        }
        data_bytes = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=5) as response:
            self.assertEqual(response.status, 200)
            body = response.read().decode('utf-8')
            res = json.loads(body)
            self.assertTrue(res["success"])
            self.assertEqual(len(res["storyboard_cuts"]), 5)
            self.assertIn("cinematic_look", res)
            self.assertIn("lut_preset", res["cinematic_look"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
