"""
Unit & Integration Tests for GENESIS Character Matting & 4-View Engine
----------------------------------------------------------------------
Tests:
1. Sheet slicing (4 equal columns)
2. Defringe & Color Decontamination (clears halo around actor)
3. Bounds detection & Ground contact pivot calculation
4. 4-View Height and ground alignment normalization
5. Input B: 4 separate photos ingestion
6. Vault catalog registration and JSON metadata verification
"""

import os
import sys
import json
import unittest
import numpy as np
from PIL import Image, ImageDraw

# Add repository root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.character_matting_engine import CharacterMattingEngine


class TestCharacterMattingEngine(unittest.TestCase):
    def setUp(self):
        self.test_vault_dir = os.path.join(os.path.dirname(__file__), "test_vault_characters")
        self.engine = CharacterMattingEngine(vault_dir=self.test_vault_dir)

    def tearDown(self):
        # Clean up test vault
        if os.path.exists(self.test_vault_dir):
            import shutil
            shutil.rmtree(self.test_vault_dir, ignore_errors=True)

    def _create_mock_sheet(self, w=1600, h=800) -> Image.Image:
        """Create a mock 4-view turnaround sheet with white background."""
        img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        col_w = w // 4

        # Draw a figure in each column with dark clothing and skin
        for i, color in enumerate([(30, 40, 60), (35, 45, 65), (25, 35, 55), (40, 50, 70)]):
            cx = i * col_w + col_w // 2
            # Head
            draw.ellipse([cx - 40, 150, cx + 40, 230], fill=(240, 200, 180, 255))
            # Body / Trenchcoat
            draw.rectangle([cx - 60, 230, cx + 60, 600], fill=(*color, 255))
            # Legs / Shoes
            draw.rectangle([cx - 45, 600, cx - 10, 720], fill=(20, 20, 20, 255))
            draw.rectangle([cx + 10, 600, cx + 45, 720], fill=(20, 20, 20, 255))

        return img

    def test_01_slice_turnaround_sheet(self):
        sheet = self._create_mock_sheet(1600, 800)
        views = self.engine.slice_turnaround_sheet(sheet)

        self.assertIn("front", views)
        self.assertIn("right", views)
        self.assertIn("back", views)
        self.assertIn("left", views)

        for name, v_img in views.items():
            self.assertEqual(v_img.size, (400, 800), f"View {name} size mismatch")

    def test_02_bounds_and_ground_pivot(self):
        # Create a sample image with transparent background
        img = Image.new("RGBA", (300, 600), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Draw actor from y=100 to y=500, x from 100 to 200
        draw.rectangle([100, 100, 200, 500], fill=(200, 50, 50, 255))

        bounds = self.engine.calculate_bounds_and_ground_pivot(img)
        self.assertEqual(bounds["top"], 100)
        self.assertEqual(bounds["bottom"], 500)
        self.assertEqual(bounds["left"], 100)
        self.assertEqual(bounds["right"], 200)
        self.assertEqual(bounds["height_px"], 401)
        # Pivot should be bottom center
        self.assertEqual(bounds["pivot"], (150, 500))

    def test_03_defringe_color_decontamination(self):
        # Create image with a white fringe on alpha edge
        img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        np_img = np.zeros((100, 100, 4), dtype=np.uint8)
        # Solid center (dark blue actor)
        np_img[30:70, 30:70] = [20, 30, 80, 255]
        # Outer halo with white residue and semitransparent alpha
        np_img[28:30, 28:72] = [255, 255, 255, 120]
        np_img[70:72, 28:72] = [255, 255, 255, 120]
        img = Image.fromarray(np_img, "RGBA")

        defringed = self.engine.defringe_color_decontamination(img)
        res_np = np.array(defringed)

        # In the halo area (29, 50), the RGB should have been decontaminated towards dark actor color
        halo_pixel_r = res_np[29, 50, 0]
        # Should be much lower than the original white 255
        self.assertLess(halo_pixel_r, 200, "Defringe failed to decontaminate white halo pixel")

    def test_04_normalize_height_and_ground(self):
        views = {}
        for v in ["front", "right", "back", "left"]:
            img = Image.new("RGBA", (300, 600), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            # Varying heights
            h_offset = 20 if v == "right" else 0
            draw.rectangle([100, 100 + h_offset, 200, 500], fill=(50, 100, 150, 255))
            views[v] = img

        norm_views, views_meta = self.engine.normalize_height_and_ground(
            views, target_canvas_size=(400, 800), target_height_ratio=0.8
        )

        self.assertEqual(len(norm_views), 4)
        for v, meta in views_meta.items():
            self.assertEqual(meta["pivot"][1], int(800 * 0.92))
            self.assertEqual(norm_views[v].size, (400, 800))

    def test_05_full_sheet_pipeline(self):
        sheet = self._create_mock_sheet(1600, 800)
        char_meta = {
            "name": "如月 蓮",
            "name_en": "Ren Kisaragi",
            "age": 26,
            "gender": "male",
            "height_m": 1.80,
            "costume_tags": ["ロングトレンチコート", "黒革靴"]
        }

        result = self.engine.process_turnaround_sheet(sheet, "ren_test_01", char_meta)
        self.assertEqual(result["id"], "ren_test_01")
        self.assertEqual(result["name"], "如月 蓮")
        self.assertIn("front", result["views"])

        # Check saved files on disk
        char_dir = os.path.join(self.test_vault_dir, "ren_test_01")
        self.assertTrue(os.path.exists(os.path.join(char_dir, "front.png")))
        self.assertTrue(os.path.exists(os.path.join(char_dir, "right.png")))
        self.assertTrue(os.path.exists(os.path.join(char_dir, "back.png")))
        self.assertTrue(os.path.exists(os.path.join(char_dir, "left.png")))
        self.assertTrue(os.path.exists(os.path.join(char_dir, "character_meta.json")))

    def test_06_individual_photos_pipeline(self):
        # 4 separate mock photos
        photos = {}
        for v in ["front", "right", "back", "left"]:
            img = Image.new("RGBA", (400, 700), (255, 255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.rectangle([120, 100, 280, 600], fill=(220, 100, 150, 255))
            photos[v] = img

        idol_meta = {
            "name": "桜木 みう",
            "name_en": "Miu Sakuragi",
            "age": 19,
            "gender": "female",
            "height_m": 1.58,
            "costume_tags": ["地下アイドル制服", "ピンクパニエ"]
        }

        result = self.engine.process_individual_photos(photos, "idol_miu_01", idol_meta)
        self.assertEqual(result["id"], "idol_miu_01")
        self.assertEqual(result["height_m"], 1.58)

        # Check listing
        char_list = self.engine.list_characters()
        self.assertTrue(any(c["id"] == "idol_miu_01" for c in char_list))


if __name__ == "__main__":
    unittest.main()
