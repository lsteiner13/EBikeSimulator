import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.physics.route_analyzer import RouteAnalyzer
from src.models.route import RoutePoint, Route

class TestRouteAnalyzer(unittest.TestCase):

    def setUp(self):
        from datetime import datetime
        
        self.p1 = RoutePoint(lat=47.2682, lon=11.3933, elevation=574, time=datetime.fromisoformat("2026-07-05T12:00:00"))
        self.p2 = RoutePoint(lat=48.1371, lon=11.5754, elevation=519, time=datetime.fromisoformat("2026-07-05T13:00:00"))
        self.p3 = RoutePoint(lat=48.2000, lon=11.6000, elevation=500, time=datetime.fromisoformat("2026-07-05T13:30:00"))
        
        test_route = Route([self.p1, self.p2, self.p3])
        self.analyzer = RouteAnalyzer(test_route)

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
    def test_summary_and_ascent(self):
        self.assertEqual(self.analyzer.total_ascent(), 0.0)
        self.assertEqual(self.analyzer.total_descent(), 74.0)
        
        summary = self.analyzer.get_summary()
        self.assertIn('total_descent_m', summary)
        self.assertIn('total_duration_s', summary)
        self.assertTrue(summary['total_duration_s'] > 0)
    
    def test_invalid_gps_coordinates(self):
        from datetime import datetime
        
        #Test ungültiger Breitengrad 
        bad_p1 = RoutePoint(lat=100.0, lon=11.3933, elevation=574, time=datetime.now())
        
        #es wird gerpürft ob das den Fehler wirft
        with self.assertRaises(ValueError):
            Route([bad_p1])

if __name__ == '__main__':
    unittest.main()