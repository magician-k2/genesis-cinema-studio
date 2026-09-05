import unittest
from core.aerial_flight_swarm_engine import AerialFlightSwarmEngine

class TestAerialFlightSwarmEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AerialFlightSwarmEngine()
        self.url1 = "https://earth.google.com/web/@34.69402084,135.50779158,14.0631779a,887.4508103d,35y,177.74049046h,67.38998674t,360r/data=..."
        self.url2 = "https://earth.google.com/web/@34.69412248,135.50146473,16.81219652a,369.34867423d,35y,177.74037796h,67.38568569t,-0r/data=..."
        self.url3 = "https://earth.google.com/web/@34.69463142,135.50123707,3.64617279a,114.21693824d,35y,177.74031514h,67.38356771t,-0r/data=..."

    def test_01_parse_google_earth_urls(self):
        wp1 = self.engine.parse_earth_url(self.url1)
        self.assertIsNotNone(wp1)
        self.assertAlmostEqual(wp1['lat'], 34.6940, places=3)
        self.assertAlmostEqual(wp1['lng'], 135.5078, places=3)
        self.assertGreater(wp1['altitude_m'], 300)

        wp2 = self.engine.parse_earth_url(self.url2)
        self.assertIsNotNone(wp2)
        self.assertGreater(wp2['altitude_m'], 100)
        self.assertLess(wp2['altitude_m'], 200)

        wp3 = self.engine.parse_earth_url(self.url3)
        self.assertIsNotNone(wp3)
        self.assertLess(wp3['altitude_m'], 60)

    def test_02_compute_dive_flight_path(self):
        wp1 = self.engine.parse_earth_url(self.url1)
        wp2 = self.engine.parse_earth_url(self.url2)
        wp3 = self.engine.parse_earth_url(self.url3)

        path = self.engine.compute_flight_path([wp1, wp2, wp3])
        self.assertEqual(path['waypoints_count'], 3)
        self.assertEqual(path['trajectory_style'], 'HYPERSONIC_SKYSCRAPER_DIVE_IN')
        self.assertGreater(path['altitude_delta_m'], 250)

    def test_03_execute_swarm_synthesis(self):
        wp1 = self.engine.parse_earth_url(self.url1)
        wp3 = self.engine.parse_earth_url(self.url3)
        path = self.engine.compute_flight_path([wp1, wp3])

        result = self.engine.execute_swarm_synthesis(
            flight_info=path,
            traffic_level='rush_hour',
            crowd_level='dense',
            location_name='大阪 中之島・市役所周辺'
        )

        self.assertTrue(result['success'])
        self.assertIn('master_veo_prompt', result)
        self.assertIn('FPV drone', result['master_veo_prompt'])
        self.assertIn('expressways', result['master_veo_prompt'])
        self.assertIn('pedestrians', result['master_veo_prompt'])
        self.assertIn('swarm_consensus', result)
        self.assertGreater(result['swarm_latency_ms'], 0)

if __name__ == '__main__':
    unittest.main()
