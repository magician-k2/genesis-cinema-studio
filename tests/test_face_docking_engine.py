import os
import sys
import unittest

ROOT_DIR = r'g:\マイドライブ\GENESIS_ROOT'
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.face_synthesis_docking_engine import face_docking_engine

class TestFaceSynthesisDocking(unittest.TestCase):
    def test_01_manifest_load(self):
        manifest = face_docking_engine.get_manifest()
        self.assertIn("men", manifest)
        self.assertIn("women", manifest)
        self.assertGreaterEqual(len(manifest["men"]), 4)
        self.assertGreaterEqual(len(manifest["women"]), 4)

    def test_02_face_assets_exist(self):
        face_vault = os.path.join(ROOT_DIR, "GENESIS_CINEMA_STUDIO", "assets", "face_vault")
        male_front = os.path.join(face_vault, "male_cool_01", "front.png")
        self.assertTrue(os.path.exists(male_front), f"Missing: {male_front}")

    def test_03_dock_trinity_execution(self):
        # Test trinity docking with ren, male_cool_01, short hair 000, male standing pose 0000
        res = face_docking_engine.dock_trinity(
            character_id="test_trinity_actor",
            face_id="male_cool_01",
            hair_category="short",
            hair_style_id="000",
            dessin_gender="male",
            dessin_category="standing",
            dessin_pose_id="0000"
        )
        self.assertTrue(res["success"])
        self.assertIn("front", res["views"])
        self.assertIn("right", res["views"])
        self.assertIn("back", res["views"])
        self.assertIn("left", res["views"])
        self.assertIn("fused_head_url", res)

        char_dir = os.path.join(ROOT_DIR, "GENESIS_CINEMA_STUDIO", "characters", "test_trinity_actor")
        self.assertTrue(os.path.exists(os.path.join(char_dir, "front.png")))
        self.assertTrue(os.path.exists(os.path.join(char_dir, "character_meta.json")))

if __name__ == '__main__':
    unittest.main()
