import math
import pandas as pd
from src.models.route import RoutePoint

class RouteAnalyzer:
    def __init__(self, points: list[RoutePoint]):
        self.points = points


    def haversine_distance(self, p1, p2):
        """Berechnet die Distanz zwischen zwei Punkten in Metern."""
        R = 6371000.0
        
        phi1, phi2 = math.radians(p1.lat), math.radians(p2.lat)
        
        delta_phi = math.radians(p2.lat - p1.lat)
        delta_lambda = math.radians(p2.lon - p1.lon)
        
        a = math.sin(delta_phi / 2.0)**2 + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2.0)**2
            
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        
        return R * c

    def total_distance(self):
        """
        Geht iterativ durch die Punkte und summiert die 
        Distanz zwischen den einzelnen GPS-Punkten auf.
        """
        total = 0.0
        
        # Schleife durch alle Zeilen bis zur vorletzten
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            
            total += self.haversine_distance(p1, p2)
            
        return total