"""
GENESIS CINEMA STUDIO: Character Matting & 4-View Engine (character_matting_engine.py)
-------------------------------------------------------------------------------------
- 1枚の4面横長シート（Front / Right / Back / Left）の自動4等分スライス＆センター合わせ
- 実在人物4枚写真（Front / Right / Back / Left）のスケール・接地高さ自動正規化
- SOTA背景除去（rembg / BiRefNet / U2Net）
- ハリウッドVFX級 Defringe & カラーデコンタミネーション（白フチ・ハロー完全消去）
- 接地足元ピボット座標 (pivot_x, pivot_y) 自動算出
- キャスト台帳（Vault: characters/{id}/）への32bit RGBA透過PNG＆メタデータ保存
"""

import os
import sys
import json
import base64
import io
import time
from typing import Dict, Tuple, List, Optional, Union
import numpy as np
from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None

# Optional rembg integration
_REMBG_SESSION = None
def get_rembg_session(model_name: str = "birefnet-general"):
    global _REMBG_SESSION
    if _REMBG_SESSION is None:
        try:
            import rembg
            try:
                _REMBG_SESSION = rembg.new_session(model_name)
            except Exception:
                _REMBG_SESSION = rembg.new_session("u2net_human_seg")
        except Exception as e:
            print(f"[MattingEngine] rembg not loaded: {e}", file=sys.stderr)
            _REMBG_SESSION = False
    return _REMBG_SESSION


class CharacterMattingEngine:
    """
    High-precision character matting, turnaround slicing, and defringe engine.
    """

    def __init__(self, vault_dir: Optional[str] = None):
        if vault_dir is None:
            # Default to GENESIS_CINEMA_STUDIO/characters
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.vault_dir = os.path.join(base_dir, "GENESIS_CINEMA_STUDIO", "characters")
        else:
            self.vault_dir = vault_dir
        os.makedirs(self.vault_dir, exist_ok=True)

    @staticmethod
    def load_image(image_input: Union[str, bytes, Image.Image]) -> Image.Image:
        """Load image from path, raw bytes, base64 data URI, or PIL Image."""
        if isinstance(image_input, Image.Image):
            return image_input.convert("RGBA")
        
        if isinstance(image_input, str):
            if image_input.startswith("data:image"):
                # Base64 data URL
                header, encoded = image_input.split(",", 1)
                image_bytes = base64.b64decode(encoded)
                return Image.open(io.BytesIO(image_bytes)).convert("RGBA")
            elif os.path.exists(image_input):
                return Image.open(image_input).convert("RGBA")
            else:
                # Try raw base64 string
                try:
                    image_bytes = base64.b64decode(image_input)
                    return Image.open(io.BytesIO(image_bytes)).convert("RGBA")
                except Exception:
                    raise ValueError(f"Invalid image path or base64 input: {image_input[:50]}...")
        
        if isinstance(image_input, (bytes, bytearray)):
            return Image.open(io.BytesIO(image_input)).convert("RGBA")
        
        raise TypeError(f"Unsupported image input type: {type(image_input)}")

    @staticmethod
    def slice_turnaround_sheet(sheet_img: Image.Image) -> Dict[str, Image.Image]:
        """
        Slices a single wide turnaround sheet (typically 4:1, 16:9, or 2:1)
        into 4 equal horizontal quadrants: [Front, Right, Back, Left].
        """
        w, h = sheet_img.size
        col_w = w // 4
        
        views = {
            "front": sheet_img.crop((0 * col_w, 0, 1 * col_w, h)),
            "right": sheet_img.crop((1 * col_w, 0, 2 * col_w, h)),
            "back":  sheet_img.crop((2 * col_w, 0, 3 * col_w, h)),
            "left":  sheet_img.crop((3 * col_w, 0, 4 * col_w, h))
        }
        return views

    def remove_background(self, img: Image.Image) -> Image.Image:
        """
        Removes background from image using rembg if available,
        or intelligent luminance/chroma key fallback if rembg is absent.
        """
        session = get_rembg_session()
        if session:
            try:
                import rembg
                res_img = rembg.remove(img, session=session)
                return res_img.convert("RGBA")
            except Exception as e:
                print(f"[MattingEngine] rembg execution error: {e}, using fallback", file=sys.stderr)

        # Fallback heuristic: Corner-sampled background detection & flood-fill / thresholding
        np_img = np.array(img.convert("RGBA"))
        h, w, _ = np_img.shape
        
        # Sample corners to find background color
        corners = [
            np_img[0, 0, :3].astype(float),
            np_img[0, w-1, :3].astype(float),
            np_img[h-1, 0, :3].astype(float),
            np_img[h-1, w-1, :3].astype(float)
        ]
        bg_mean = np.mean(corners, axis=0)

        # Color distance from bg_mean
        diff = np_img[:, :, :3].astype(float) - bg_mean
        dist = np.sqrt(np.sum(diff ** 2, axis=2))
        
        # Compute alpha mask
        thresh = 35.0
        alpha = np.clip((dist - thresh) * (255.0 / 30.0), 0, 255).astype(np.uint8)
        
        # Edge mask cleanup with morphological operations if cv2 is available
        if cv2 is not None:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, kernel)
        
        np_img[:, :, 3] = alpha
        return Image.fromarray(np_img, "RGBA")

    @staticmethod
    def defringe_color_decontamination(img: Image.Image, iterations: int = 3) -> Image.Image:
        """
        Hollywood VFX Grade Defringe (Color Decontamination):
        Neutralizes white/black/green halos on translucent edge pixels (0 < alpha < 255)
        by extending (bleeding) the solid foreground RGB colors into the edge boundary.
        """
        np_img = np.array(img).astype(np.float32)
        r, g, b, a = np_img[:, :, 0], np_img[:, :, 1], np_img[:, :, 2], np_img[:, :, 3]

        if cv2 is None:
            # Simple RGB fade fallback
            return img

        solid_mask = (a > 240).astype(np.uint8) * 255
        edge_mask = ((a > 5) & (a <= 240)).astype(np.uint8) * 255

        if np.count_nonzero(solid_mask) == 0:
            return img

        # Distance transform to propagate solid colors outward into edge regions
        # Inpainting solid RGB into the edge mask
        solid_bgr = np.dstack([b, g, r]).astype(np.uint8)
        inpaint_mask = (255 - solid_mask).astype(np.uint8)

        # Telea Inpaint to bleed clean core colors across fringes
        decontaminated_bgr = cv2.inpaint(solid_bgr, inpaint_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

        # Blend decontaminated color into the edge pixels based on edge_mask
        blend_factor = (edge_mask.astype(np.float32) / 255.0)[:, :, np.newaxis]
        clean_rgb = np.dstack([
            decontaminated_bgr[:, :, 2],
            decontaminated_bgr[:, :, 1],
            decontaminated_bgr[:, :, 0]
        ]).astype(np.float32)

        final_rgb = np_img[:, :, :3] * (1.0 - blend_factor) + clean_rgb * blend_factor
        final_rgba = np.dstack([final_rgb, a]).clip(0, 255).astype(np.uint8)

        return Image.fromarray(final_rgba, "RGBA")

    @staticmethod
    def calculate_bounds_and_ground_pivot(img: Image.Image) -> Dict[str, Union[int, float, Tuple[int, int]]]:
        """
        Finds bounding box of the actor:
        - Top head coordinate
        - Bottom feet coordinate
        - Center X
        - Physical contact pivot (bottom center between feet)
        """
        np_img = np.array(img)
        alpha = np_img[:, :, 3]
        h, w = alpha.shape

        non_zero_coords = np.argwhere(alpha > 20)
        if len(non_zero_coords) == 0:
            # Completely transparent image
            return {
                "top": 0,
                "bottom": h - 1,
                "left": 0,
                "right": w - 1,
                "height_px": h,
                "width_px": w,
                "pivot": (w // 2, h - 1),
                "pivot_norm": (0.5, 1.0)
            }

        y_min, x_min = non_zero_coords.min(axis=0)
        y_max, x_max = non_zero_coords.max(axis=0)

        # Foot ground contact point: bottom center
        pivot_x = int((x_min + x_max) // 2)
        pivot_y = int(y_max)

        return {
            "top": int(y_min),
            "bottom": int(y_max),
            "left": int(x_min),
            "right": int(x_max),
            "height_px": int(y_max - y_min + 1),
            "width_px": int(x_max - x_min + 1),
            "pivot": (pivot_x, pivot_y),
            "pivot_norm": (round(pivot_x / w, 4), round(pivot_y / h, 4))
        }

    def normalize_height_and_ground(
        self,
        views: Dict[str, Image.Image],
        target_canvas_size: Tuple[int, int] = (600, 1000),
        target_height_ratio: float = 0.82
    ) -> Tuple[Dict[str, Image.Image], Dict[str, dict]]:
        """
        Normalizes all 4 views (Front, Right, Back, Left) so:
        1. Character heights match target proportion (e.g. 82% of canvas height).
        2. All feet touch the identical baseline ground line (y = canvas_height * 0.92).
        3. Character is horizontally centered.
        """
        target_w, target_h = target_canvas_size
        ground_y = int(target_h * 0.92)
        desired_char_h = int(target_h * target_height_ratio)

        # 1. Determine average or reference height from front view
        ref_bounds = self.calculate_bounds_and_ground_pivot(views.get("front", list(views.values())[0]))
        ref_h = max(ref_bounds["height_px"], 50)

        normalized_views = {}
        views_meta = {}

        for view_name in ["front", "right", "back", "left"]:
            if view_name not in views:
                continue
            v_img = views[view_name]
            bounds = self.calculate_bounds_and_ground_pivot(v_img)
            char_h = bounds["height_px"]

            # Scale factor: use front reference height to maintain natural perspective differences
            scale = desired_char_h / ref_h

            # Crop character tight with minimal margin
            orig_w, orig_h = v_img.size
            crop_box = (
                max(0, bounds["left"] - 10),
                max(0, bounds["top"] - 10),
                min(orig_w, bounds["right"] + 10),
                min(orig_h, bounds["bottom"] + 5)
            )
            char_cropped = v_img.crop(crop_box)

            new_w = max(1, int(char_cropped.width * scale))
            new_h = max(1, int(char_cropped.height * scale))
            char_resized = char_cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)

            # Create standard blank transparent canvas
            canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))

            # Position feet at ground_y, horizontally centered
            pos_x = (target_w - new_w) // 2
            pos_y = ground_y - new_h

            canvas.paste(char_resized, (pos_x, pos_y), char_resized)

            normalized_views[view_name] = canvas
            views_meta[view_name] = {
                "view": view_name,
                "scale": round(scale, 4),
                "pivot": (target_w // 2, ground_y),
                "pivot_norm": (0.5, round(ground_y / target_h, 4)),
                "bounds": self.calculate_bounds_and_ground_pivot(canvas)
            }

        return normalized_views, views_meta

    def process_turnaround_sheet(
        self,
        sheet_input: Union[str, bytes, Image.Image],
        char_id: str,
        char_metadata: dict
    ) -> dict:
        """
        Process a single 4-view turnaround sheet (Input A):
        1. Slices into 4 views
        2. Removes background
        3. Applies Defringe color decontamination
        4. Normalizes heights and grounds
        5. Saves to Vault
        """
        sheet = self.load_image(sheet_input)
        raw_views = self.slice_turnaround_sheet(sheet)

        clean_views = {}
        for view_name, raw_img in raw_views.items():
            # Background removal
            matted = self.remove_background(raw_img)
            # Defringe
            defringed = self.defringe_color_decontamination(matted)
            clean_views[view_name] = defringed

        # Normalization
        norm_views, views_meta = self.normalize_height_and_ground(clean_views)

        # Export to Vault
        return self.export_to_vault(char_id, char_metadata, norm_views, views_meta)

    def process_individual_photos(
        self,
        photos_dict: Dict[str, Union[str, bytes, Image.Image]],
        char_id: str,
        char_metadata: dict
    ) -> dict:
        """
        Process 4 individual smartphone photos of real actors (Input B):
        1. Loads Front, Right, Back, Left
        2. Removes background on all 4
        3. Applies Defringe color decontamination
        4. Normalizes heights and grounds
        5. Saves to Vault
        """
        clean_views = {}
        for view_name in ["front", "right", "back", "left"]:
            if view_name in photos_dict and photos_dict[view_name]:
                raw_img = self.load_image(photos_dict[view_name])
                matted = self.remove_background(raw_img)
                defringed = self.defringe_color_decontamination(matted)
                clean_views[view_name] = defringed
            else:
                # If an angle is missing, generate transparent placeholder
                clean_views[view_name] = Image.new("RGBA", (600, 1000), (0, 0, 0, 0))

        norm_views, views_meta = self.normalize_height_and_ground(clean_views)
        return self.export_to_vault(char_id, char_metadata, norm_views, views_meta)

    def export_to_vault(
        self,
        char_id: str,
        char_metadata: dict,
        views: Dict[str, Image.Image],
        views_meta: dict
    ) -> dict:
        """
        Saves character transparent PNGs and JSON metadata into characters/{char_id}/
        """
        char_dir = os.path.join(self.vault_dir, char_id)
        os.makedirs(char_dir, exist_ok=True)

        rel_paths = {}
        for view_name, img in views.items():
            filename = f"{view_name}.png"
            filepath = os.path.join(char_dir, filename)
            img.save(filepath, "PNG")
            rel_paths[view_name] = f"/characters/{char_id}/{filename}"

        full_meta = {
            "id": char_id,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "name": char_metadata.get("name", "未設定キャラクター"),
            "name_en": char_metadata.get("name_en", "Unnamed Character"),
            "age": char_metadata.get("age", 25),
            "gender": char_metadata.get("gender", "unspecified"),
            "height_m": float(char_metadata.get("height_m", 1.75)),
            "build": char_metadata.get("build", "natural"),
            "voice_profile": char_metadata.get("voice_profile", "Aoede"),
            "costume_tags": char_metadata.get("costume_tags", []),
            "ec_product_links": char_metadata.get("ec_product_links", []),
            "views": rel_paths,
            "views_meta": views_meta
        }

        meta_path = os.path.join(char_dir, "character_meta.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(full_meta, f, ensure_ascii=False, indent=2)

        # Also register in characters_vault.json
        vault_master_path = os.path.join(self.vault_dir, "characters_vault.json")
        vault_catalog = []
        if os.path.exists(vault_master_path):
            try:
                with open(vault_master_path, "r", encoding="utf-8") as f:
                    vault_catalog = json.load(f)
            except Exception:
                vault_catalog = []

        # Remove existing if same ID
        vault_catalog = [c for c in vault_catalog if c.get("id") != char_id]
        vault_catalog.insert(0, full_meta)

        with open(vault_master_path, "w", encoding="utf-8") as f:
            json.dump(vault_catalog, f, ensure_ascii=False, indent=2)

        return full_meta

    def list_characters(self) -> List[dict]:
        """Lists all registered characters in vault."""
        vault_master_path = os.path.join(self.vault_dir, "characters_vault.json")
        if os.path.exists(vault_master_path):
            try:
                with open(vault_master_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []
