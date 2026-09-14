# -*- coding: utf-8 -*-
"""
🎬 GENESIS Audio-to-Cinema Synchronized Video Director Engine
=============================================================
Deconstructs audio timbre (spectral centroid, warmth, roughness, transients)
and song structure (Intro, Verse, Build-up, Chorus/Drop, Outro) to generate
fully synchronized cinematic scene cuts, camera motion, color LUTs, and
video prompts tailored for Google Veo 3.1, Runway Gen-3, and Agentic Video.
"""

import os
import sys
import json
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from core.neural_backbone.gemini_hub import gemini_hub
except ImportError:
    gemini_hub = None

def analyze_timbre_to_cinematic_look(features: dict) -> dict:
    """
    Translates physical acoustic timbre metrics into cinematic photography & lighting specs.
    
    Acoustic Metrics:
    - spectral_centroid: Brightness (Hz)
    - spectral_rolloff: High frequency presence (Hz)
    - spectral_flatness: Noise vs Tonal purity (0.0 - 1.0)
    - percussive_ratio: Percussive transients vs Harmonic resonance
    - sub_bass_ratio: Low-end energy (<150Hz)
    """
    centroid = features.get("spectral_centroid", 2500.0)
    flatness = features.get("spectral_flatness", 0.01)
    perc_ratio = features.get("percussive_ratio", 0.4)
    sub_ratio = features.get("sub_bass_ratio", 0.3)
    bpm = features.get("bpm", 120.0)
    key = features.get("key", "C Major")

    # 1. Lens & Camera Setup
    if centroid < 1800:
        lens = "ARRI Master Anamorphic 50mm T1.9 (Deep cinematic focal falloff, warm anamorphic bokeh)"
        shutter = "1/48s cinematic standard, natural organic motion blur"
    elif centroid > 3200:
        lens = "Cooke S4/i Prime 25mm T2.0 (Ultra-sharp edge-to-edge, punchy geometric contrast)"
        shutter = "1/96s high-speed shutter, crisp dynamic action transients"
    else:
        lens = "Zeiss Supreme Prime 35mm T1.5 (Balanced portrait-to-environment spatial depth)"
        shutter = "1/48s 180-degree shutter rule"

    # 2. Color Grading & LUT
    if "Minor" in key or sub_ratio > 0.4:
        color_palette = "Cyberpunk Noir: Midnight Obsidian (#070a12), Cold Neon Cyan (#06b6d4), Deep Blood Amber (#f97316)"
        lut_preset = "Kodak 2383 Bleach Bypass + Teal & Deep Orange Shadows"
        grain = "Fine 35mm Vision3 500T organic film grain"
    elif centroid > 3000:
        color_palette = "High-Voltage Acid: Electric Purple (#a855f7), Laser Turquoise (#14b8a6), Strobe Silver (#f8fafc)"
        lut_preset = "Fuji ETERNA Vivid Cross-Process"
        grain = "Ultra-clean digital sensor, pinpoint specular glints"
    else:
        color_palette = "Golden Cinematic: Warm Honey (#f59e0b), Velvet Charcoal (#18181b), Diffused Pearl (#fef3c7)"
        lut_preset = "Kodak Portra 400 Soft Golden Hour Warmth"
        grain = "Subtle 16mm organic analog warmth"

    # 3. Lighting Style
    if flatness > 0.02 or perc_ratio > 0.55:
        lighting = "Aggressive Chiaroscuro with harsh rhythmic strobe flashes and industrial sodium-vapor practicals"
    elif sub_ratio > 0.35:
        lighting = "Heavy volumetric atmospheric fog, low-angle ground rim lights, silhouetted high-contrast backlights"
    else:
        lighting = "Soft wrap-around key light through 8x8 diffusion silk, gentle ambient fill, subtle cinematic haze"

    # 4. Cinematic Rhythm
    if bpm >= 135:
        rhythm_profile = "Kinetic Fast-Cut (Average shot duration: 1.5 - 2.5s, whip-pans, snap zooms)"
    elif bpm >= 105:
        rhythm_profile = "Steadicam Driving Flow (Average shot duration: 3.5 - 5.0s, push-in dollies, dynamic tracking)"
    else:
        rhythm_profile = "Atmospheric Contemplative (Average shot duration: 6.0 - 10.0s, slow crane descents, micro-drifts)"

    return {
        "lens_choice": lens,
        "shutter_speed": shutter,
        "color_palette": color_palette,
        "lut_preset": lut_preset,
        "film_grain": grain,
        "lighting_setup": lighting,
        "cinematic_rhythm": rhythm_profile,
        "timbre_summary": f"Centroid: {centroid}Hz | Sub-bass: {int(sub_ratio*100)}% | Percussive: {int(perc_ratio*100)}%"
    }

def decompose_song_structure(features: dict, total_duration_sec: float = 60.0) -> list:
    """
    Decomposes song into structured dramatic sections (Intro, Verse, Build-up, Chorus/Drop, Outro)
    with precise second boundaries and dramatic intensity.
    """
    bpm = features.get("bpm", 120.0)
    dur = float(total_duration_sec) if total_duration_sec and total_duration_sec > 10 else 60.0

    # Calculate bar length in seconds (4 beats per bar)
    seconds_per_beat = 60.0 / max(40.0, min(240.0, bpm))
    bar_sec = seconds_per_beat * 4.0

    # Section proportion heuristic based on standard musical form
    intro_len = max(4.0, round(bar_sec * 2, 1))
    outro_len = max(4.0, round(bar_sec * 2, 1))
    remaining = max(10.0, dur - intro_len - outro_len)

    # 3 core internal sections: Verse, Build-up, Chorus/Drop
    verse_len = round(remaining * 0.4, 1)
    buildup_len = round(remaining * 0.25, 1)
    drop_len = round(remaining - verse_len - buildup_len, 1)

    t0 = 0.0
    t1 = round(t0 + intro_len, 1)
    t2 = round(t1 + verse_len, 1)
    t3 = round(t2 + buildup_len, 1)
    t4 = round(t3 + drop_len, 1)
    t5 = round(dur, 1)

    sections = [
        {
            "section": "Intro",
            "start_sec": t0,
            "end_sec": t1,
            "duration_sec": round(t1 - t0, 1),
            "energy_level": 25,
            "musical_role": "Ambient atmosphere, motif statement, rhythmic establishment",
            "dramatic_intent": "World-building, establishing spatial scale and emotional loneliness",
            "shot_type": "Extreme Wide Establishing Shot (EWS)",
            "camera_motion": "Slow aerial crane drift lowering from stormy skyline toward wet street"
        },
        {
            "section": "Verse 1",
            "start_sec": t1,
            "end_sec": t2,
            "duration_sec": round(t2 - t1, 1),
            "energy_level": 50,
            "musical_role": "Groove kicks in, melodic narrative progression, steady rhythm",
            "dramatic_intent": "Introducing protagonist (如月 蓮 / Ren), quiet determination in motion",
            "shot_type": "Medium Full Shot (MFS) Tracking",
            "camera_motion": "Steadicam lateral tracking walking alongside character in trenchcoat"
        },
        {
            "section": "Build-up (Rise)",
            "start_sec": t2,
            "end_sec": t3,
            "duration_sec": round(t3 - t2, 1),
            "energy_level": 78,
            "musical_role": "Snare roll acceleration, rising filter resonance, tension crescendo",
            "dramatic_intent": "Anticipation, ticking clock urgency, preparing for the breakthrough",
            "shot_type": "Close-Up (CU) & Dutch Angle Jib",
            "camera_motion": "Rapid push-in zoom into character eyes reflecting glowing AR interface"
        },
        {
            "section": "Chorus / Drop",
            "start_sec": t3,
            "end_sec": t4,
            "duration_sec": round(t4 - t3, 1),
            "energy_level": 100,
            "musical_role": "Full harmonic explosion, maximum sub-bass impact, soaring lead",
            "dramatic_intent": "Cathartic release, high-speed movement, visual spectacle, awakening",
            "shot_type": "360-degree Orbit & Low-Angle Dynamic Hero Shot",
            "camera_motion": "High-velocity arc rotation with anamorphic lens streaks and volumetric flares"
        },
        {
            "section": "Outro",
            "start_sec": t4,
            "end_sec": t5,
            "duration_sec": round(t5 - t4, 1),
            "energy_level": 30,
            "musical_role": "Reverb decay, fading rhythm, lingering melodic echo",
            "dramatic_intent": "Lingering consequence, gazing into the dawn horizon, resolution",
            "shot_type": "Wide Low-Angle Locked-Off Shot",
            "camera_motion": "Slow reverse pull-back disappearing into cinematic smoke and rain"
        }
    ]

    return sections

def generate_synchronized_cinema_storyboard(features: dict, track_title: str = "GENESIS Master Track", scene_context: str = "サイバー東京ノワール", total_duration_sec: float = 60.0) -> dict:
    """
    Main Director Pipeline:
    Fuses Timbre Look + Song Structure + Character Vault to produce an executive NLE Storyboard.
    """
    look = analyze_timbre_to_cinematic_look(features)
    sections = decompose_song_structure(features, total_duration_sec=total_duration_sec)
    
    bpm = features.get("bpm", 120.0)
    key = features.get("key", "D Minor")
    
    # Enrich each section with ready-to-render AI Video Prompts (Veo 3.1 & Runway Gen-3)
    storyboard_cuts = []
    for idx, sec in enumerate(sections, 1):
        prompt_veo = (
            f"Cinematic 35mm film still, {sec['shot_type']}, {sec['camera_motion']}. "
            f"Scene: {scene_context}, protagonist Ren in noir cyber-trenchcoat. "
            f"Lighting: {look['lighting_setup']}. Color Grade: {look['lut_preset']}. "
            f"Musical sync: {sec['section']} at {bpm}BPM in {key}, {look['shutter_speed']}. "
            f"Masterpiece 8K resolution, photorealistic ARRI Alexa LF aesthetic, authentic depth of field."
        )
        
        storyboard_cuts.append({
            "cut_id": f"CUT_{idx:02d}",
            "section": sec["section"],
            "timecode": f"{int(sec['start_sec']//60):02d}:{int(sec['start_sec']%60):02d} - {int(sec['end_sec']//60):02d}:{int(sec['end_sec']%60):02d}",
            "start_sec": sec["start_sec"],
            "end_sec": sec["end_sec"],
            "duration_sec": sec["duration_sec"],
            "energy_level": sec["energy_level"],
            "musical_role": sec["musical_role"],
            "dramatic_intent": sec["dramatic_intent"],
            "shot_type": sec["shot_type"],
            "camera_motion": sec["camera_motion"],
            "video_generation_prompt": prompt_veo
        })

    return {
        "success": True,
        "track_title": track_title,
        "total_duration_sec": total_duration_sec,
        "bpm": bpm,
        "key": key,
        "cinematic_look": look,
        "storyboard_cuts": storyboard_cuts,
        "director_note": f"Audio timbre successfully translated into {look['lut_preset']} with {len(storyboard_cuts)} synchronized cuts."
    }

if __name__ == "__main__":
    test_feat = {
        "bpm": 128.0,
        "key": "A Minor",
        "spectral_centroid": 2800.0,
        "spectral_flatness": 0.015,
        "percussive_ratio": 0.48,
        "sub_bass_ratio": 0.38
    }
    res = generate_synchronized_cinema_storyboard(test_feat, "Techno Pulse", "雨のサイバーパンク新宿")
    print(f"Generated {len(res['storyboard_cuts'])} synchronized cuts.")
    print(f"Look: {res['cinematic_look']['lut_preset']}")
