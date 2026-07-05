import math
from datetime import datetime
# from src.models.route import RoutePoint # (Falls dein Kollege das hier stehen hatte, lass es drin, Python braucht es hier aber nicht zwingend für die Logik)

class RouteAnalyzer:
    def __init__(self, points):
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
        """Summiert die Distanz zwischen den einzelnen GPS-Punkten auf."""
        total = 0.0
        for i in range(len(self.points) - 1):
            total += self.haversine_distance(self.points[i], self.points[i+1])
        return total

    def get_speeds(self):
        """Berechnet die Geschwindigkeit (in km/h) für jeden Streckenabschnitt."""
        speeds = []
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            
            dist = self.haversine_distance(p1, p2) # in Metern
            
            # Zeitstempel auslesen und Differenz in Sekunden berechnen
            # .replace('Z', '+00:00') stellt sicher, dass das Format korrekt gelesen wird
            t1 = datetime.fromisoformat(p1.time.replace('Z', '+00:00'))
            t2 = datetime.fromisoformat(p2.time.replace('Z', '+00:00'))
            
            time_diff_seconds = (t2 - t1).total_seconds()
            
            if time_diff_seconds > 0:
                speed_mps = dist / time_diff_seconds # Meter pro Sekunde
                speed_kmh = speed_mps * 3.6          # Umrechnung in km/h
            else:
                speed_kmh = 0.0
                
            speeds.append(speed_kmh)
            
        return speeds

    def average_speed(self):
        """Berechnet die Durchschnittsgeschwindigkeit der gesamten Route in km/h."""
        if len(self.points) < 2:
            return 0.0
            
        total_dist = self.total_distance()
        
        t_start = datetime.fromisoformat(self.points[0].time.replace('Z', '+00:00'))
        t_end = datetime.fromisoformat(self.points[-1].time.replace('Z', '+00:00'))
        
        total_time_seconds = (t_end - t_start).total_seconds()
        
        if total_time_seconds > 0:
            return (total_dist / total_time_seconds) * 3.6
        return 0.0

    def max_speed(self):
        """Ermittelt die Maximalgeschwindigkeit in km/h."""
        speeds = self.get_speeds()
        if not speeds:
            return 0.0
        return max(speeds)