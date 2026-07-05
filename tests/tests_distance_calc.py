import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from physics.route_analyzer import RouteAnalyzer
from models.route import RoutePoint

class TestRouteAnalyzer(unittest.TestCase):

    def setUp(self):
        # 3 Punkte für Tests (Innsbruck, München, und ein dritter fiktiver Punkt)
        self.p1 = RoutePoint(lat=47.2682, lon=11.3933, elevation=574, time="2026-07-05T12:00:00Z")
        self.p2 = RoutePoint(lat=48.1371, lon=11.5754, elevation=519, time="2026-07-05T13:00:00Z")
        self.p3 = RoutePoint(lat=48.2000, lon=11.6000, elevation=500, time="2026-07-05T13:30:00Z")
        self.analyzer = RouteAnalyzer([self.p1, self.p2, self.p3])

    def test_total_distance(self):
        total_dist = self.analyzer.total_distance()
        self.assertTrue(total_dist > 97000)

    def test_speeds(self):
        speeds = self.analyzer.get_speeds()
        self.assertEqual(len(speeds), 2) 
        self.assertTrue(speeds[0] > 0)
        
    def test_accelerations(self):
        accels = self.analyzer.get_accelerations()
        self.assertEqual(len(accels), 1) 
        
        max_accel = self.analyzer.max_acceleration()
        self.assertIsInstance(max_accel, float)
    
    def test_elevation_data(self):
        data = self.analyzer.get_elevation_data()
        
        self.assertEqual(len(data), 2)
        
        self.assertIn('dh', data[0])
        self.assertIn('gradient_percent', data[0])
        self.assertIn('angle_degrees', data[0])
        
        self.assertEqual(data[0]['dh'], -55.0)

if __name__ == '__main__':
    unittest.main()