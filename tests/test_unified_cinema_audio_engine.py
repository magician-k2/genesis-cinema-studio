import os
import unittest
import subprocess
import json

class TestUnifiedCinemaAudioEngine(unittest.TestCase):
    def setUp(self):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.cinema_dir = os.path.join(self.root_dir, 'GENESIS_CINEMA_STUDIO')
        self.engine_js = os.path.join(self.cinema_dir, 'genesis_unified_cinema_audio_engine.js')
        self.music_studio = os.path.join(self.cinema_dir, 'music_studio.html')
        self.cinema_lite = os.path.join(self.cinema_dir, 'cinema_lite.html')

    def test_shared_engine_file_exists(self):
        self.assertTrue(os.path.exists(self.engine_js), 'genesis_unified_cinema_audio_engine.js must exist')
        with open(self.engine_js, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('class GenesisCinemaAudioEngine', content)
        self.assertIn('window.genesisCinemaAudio', content)
        self.assertIn('genesis_nervous_bus', content)

    def test_shared_engine_node_runtime(self):
        node_script = (
            "const { GenesisCinemaAudioEngine } = require('./GENESIS_CINEMA_STUDIO/genesis_unified_cinema_audio_engine.js');\n"
            "const engine = new GenesisCinemaAudioEngine();\n"
            "const mockStoryboard = {\n"
            "    storyboard_cuts: [\n"
            "        { cut_id: 'CUT_01', section: 'Intro', timecode: '00:00 - 00:04', shot_type: 'EWS', camera_motion: 'Crane Down', video_generation_prompt: 'Veo Cut 1', gemini_omni_prompt: 'Omni Cut 1' },\n"
            "        { cut_id: 'CUT_02', section: 'Verse', timecode: '00:04 - 00:20', shot_type: 'MFS', camera_motion: 'Steadicam', video_generation_prompt: 'Veo Cut 2', gemini_omni_prompt: 'Omni Cut 2' }\n"
            "    ],\n"
            "    cinematic_look: { lut_preset: 'Kodak Portra 400', lens_choice: '35mm T1.5' }\n"
            "};\n"
            "const prompts = engine.formatPrompts(mockStoryboard);\n"
            "console.log(JSON.stringify({\n"
            "    busName: engine.busName,\n"
            "    storageKey: engine.storageKey,\n"
            "    veoLength: prompts.veo.length,\n"
            "    agenticLength: prompts.agentic.length,\n"
            "    cutsCount: prompts.cuts.length\n"
            "}));\n"
        )
        res = subprocess.run(['node', '-e', node_script], cwd=self.root_dir, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout.strip())
        self.assertEqual(data['busName'], 'genesis_nervous_bus')
        self.assertEqual(data['storageKey'], 'genesis_active_storyboard')
        self.assertGreater(data['veoLength'], 20)
        self.assertGreater(data['agenticLength'], 20)
        self.assertEqual(data['cutsCount'], 2)

    def test_html_files_include_shared_engine(self):
        with open(self.music_studio, 'r', encoding='utf-8') as f:
            music_html = f.read()
        self.assertIn('genesis_unified_cinema_audio_engine.js', music_html)
        self.assertIn('genesisCinemaAudio', music_html)

        with open(self.cinema_lite, 'r', encoding='utf-8') as f:
            cinema_html = f.read()
        self.assertIn('genesis_unified_cinema_audio_engine.js', cinema_html)
        self.assertIn('genesisCinemaAudio', cinema_html)

if __name__ == '__main__':
    unittest.main()
