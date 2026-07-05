import unittest
from datetime import datetime

from src.models.route import Route, RoutePoint
from src.physics.route_analyzer import RouteAnalyzer

class TestRouteAnalyzer(unittest.TestCase):

    def setUp(self):
        """Test-Route mit 3 Punkten erstellen"""

        self.route = Route([
            RoutePoint(
                lat=47.2682,
                lon=11.3933,
                elevation=0.0,
                time=datetime(2024, 1, 1, 12, 0, 0)
            ),
            RoutePoint(
                lat=47.5000,
                lon=11.4500,
                elevation=50.0,
                time=datetime(2024, 1, 1, 12, 10, 0)
            ),
            RoutePoint(
                lat=48.1371,
                lon=11.5754,
                elevation=200.0,
                time=datetime(2024, 1, 1, 12, 20, 0)
            ),
        ])

        self.analyzer = RouteAnalyzer(self.route.points)

    # -----------------------------------------------------

    def test_haversine_distance(self):
        """Testet Distanz zwischen zwei Punkten"""

        p1 = self.route.points[0]
        p2 = self.route.points[1]

        dist = self.analyzer.haversine_distance(p1, p2)

        self.assertIsInstance(dist, float)
        self.assertGreater(dist, 0)

        # grobe Plausibilitätsgrenze (Innsbruck ~ München ~ 100 km)
        self.assertLess(dist, 200000)

    # -----------------------------------------------------

    def test_total_distance(self):
        """Testet Gesamtstrecke der Route"""

        total = self.analyzer.total_distance()

        self.assertIsInstance(total, float)
        self.assertGreater(total, 0)

    # -----------------------------------------------------

    def test_route_length(self):
        """Testet ob Route korrekt aufgebaut ist"""

        self.assertEqual(len(self.route.points), 3)

    # -----------------------------------------------------
