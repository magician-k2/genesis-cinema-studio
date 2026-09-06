import unittest
import urllib.request
import json
import time
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.aerial_flight_swarm_engine import AerialFlightSwarmEngine

class TestFullCinemaEcosystemSwarm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://localhost:8080"
        cls.swarm_engine = AerialFlightSwarmEngine()

    def test_01_all_cinema_studio_screens_http_status(self):
        screens = [
            "/index.html",
            "/cast_footage_studio.html",
            "/aerial_studio.html",
            "/media_vault.html",
            "/asset_studio.html",
            "/storyboard_studio.html",
            "/video_player.html",
            "/audio_mixer.html"
        ]
        for screen in screens:
            url = f"{self.base_url}{screen}"
            req = urllib.request.Request(url, headers={'User-Agent': 'GenesisSwarmTester/1.0'})
            success = False
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(req, timeout=5) as res:
                        self.assertEqual(res.status, 200, f"Screen {screen} returned status {res.status}")
                        success = True
                        break
                except Exception:
                    time.sleep(0.3)
            self.assertTrue(success, f"Failed to access {screen} after 3 attempts")

    def test_02_media_vault_aggregation_api(self):
        url = f"{self.base_url}/api/media_vault"
        req = urllib.request.Request(url, headers={'User-Agent': 'GenesisSwarmTester/1.0'})
        with urllib.request.urlopen(req, timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode('utf-8'))
            self.assertTrue(data.get('success'))
            assets = data.get('assets', [])
            self.assertGreaterEqual(len(assets), 10)
            categories = {a.get('category') for a in assets}
            self.assertIn('cast', categories)
            self.assertIn('costume', categories)
            self.assertIn('prop', categories)
            self.assertIn('vehicle', categories)
            self.assertIn('aerial', categories)
            self.assertIn('footage', categories)

    def test_03_media_vault_new_asset_post_and_retrieve(self):
        url = f"{self.base_url}/api/media_vault"
        test_item = {
            'id': f"test_e2e_asset_{int(time.time())}",
            'title': 'E2E 自動検証用ネオン小道具',
            'category': 'prop',
            'category_name': '小道具',
            'thumbnail': 'https://images.unsplash.com/photo-1544441893-675973e31985?w=500',
            'tags': ['E2Eテスト', '自動検証'],
            'source_studio': 'test_suite'
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(test_item).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode('utf-8'))
            self.assertTrue(data.get('success'))

    def test_04_upgraded_16_agent_swarm_parallel_synthesis(self):
        self.assertEqual(len(self.swarm_engine.swarm_roles), 16)
        flight_metrics = {
            'start_altitude_m': 355.0,
            'end_altitude_m': 48.0,
            'flight_duration_s': 5.5,
            'trajectory_style': 'HYPERSONIC_SKYSCRAPER_DIVE_IN'
        }
        result = self.swarm_engine.execute_swarm_synthesis(
            flight_info=flight_metrics,
            traffic_level='rush_hour',
            crowd_level='dense',
            location_name='大阪 中之島・堂島リバーフロント',
            landing_gimmick='orbit_360',
            hero_name='如月 蓮'
        )

        self.assertTrue(result['success'])
        self.assertEqual(result['swarm_agent_count'], 16)
        consensus = result['swarm_consensus']
        self.assertIn('lighting_cortex', consensus)
        self.assertIn('camera_physics', consensus)
        self.assertIn('weather_dynamics', consensus)
        self.assertIn('vehicle_texture_mapper', consensus)
        self.assertIn('spatial_audio_director', consensus)
        self.assertIn('cloud_burst_dispatcher', consensus)
        self.assertIn('dam_indexer', consensus)
        self.assertIn("Cinematic 35mm", result['master_veo_prompt'])
        self.assertIn("orbit", result['master_veo_prompt'].lower())
        self.assertLess(result['swarm_latency_ms'], 100.0)

    def test_05_aerial_flight_video_recording_analyzer(self):
        res = self.swarm_engine.analyze_flight_video(
            video_name="flight_dive_osaka.mp4",
            duration_s=6.5,
            estimated_start_alt=400.0,
            estimated_end_alt=50.0
        )
        self.assertTrue(res['success'])
        self.assertEqual(len(res['waypoints']), 4)
        self.assertEqual(res['waypoints'][0]['stage'], 'HIGH_CRUISE')
        self.assertEqual(res['waypoints'][3]['stage'], 'STREET_LANDING')

if __name__ == '__main__':
    unittest.main()
