import unittest
import json
import urllib.request
import urllib.parse
import os
import sys

class TestSceneComposerAPI(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:8080'

    def test_01_get_scene_assets(self):
        req = urllib.request.Request(f'{self.BASE_URL}/api/scene/assets')
        with urllib.request.urlopen(req, timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode('utf-8'))
            self.assertIn('costumes', data)
            self.assertIn('props', data)
            self.assertIn('vehicles', data)
            self.assertGreater(len(data['costumes']), 0)
            self.assertGreater(len(data['props']), 0)
            self.assertGreater(len(data['vehicles']), 0)

    def test_02_generate_scene(self):
        payload = {
            'character_id': 'test_ren_e2e',
            'costume_id': 'costume_trench_01',
            'prop_id': 'prop_umbrella_01',
            'vehicle_id': 'veh_toei_bus_01',
            'location': {
                'lat': 35.7111,
                'lng': 139.7963,
                'locationName': '浅草寺 雷門',
                'heading': 180,
                'isAlleyway': True
            },
            'custom_prompt': 'Atmospheric rain sequence'
        }
        req = urllib.request.Request(
            f'{self.BASE_URL}/api/scene/generate',
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode('utf-8'))
            self.assertTrue(data.get('success'))
            self.assertIn('veo_prompt', data)
            self.assertIn('trench coat', data['veo_prompt'])
            self.assertIn('umbrella', data['veo_prompt'])
            self.assertIn('city transit bus', data['veo_prompt'])
            self.assertIn('preview_layers', data)

    def test_03_get_scenes_vault(self):
        req = urllib.request.Request(f'{self.BASE_URL}/api/scenes')
        with urllib.request.urlopen(req, timeout=5) as res:
            self.assertEqual(res.status, 200)
            scenes = json.loads(res.read().decode('utf-8'))
            self.assertIsInstance(scenes, list)
            self.assertGreater(len(scenes), 0)

if __name__ == '__main__':
    unittest.main()
