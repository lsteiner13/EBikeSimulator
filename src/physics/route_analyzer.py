import math
from datetime import datetime


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
    
    def get_accelerations(self):
        """
        Berechnet die Beschleunigung (in m/s²) zwischen den Streckenabschnitten.
        Benötigt mindestens 3 GPS-Punkte (2 Geschwindigkeits-Intervalle).
        """
        speeds_kmh = self.get_speeds()
        accelerations = []
        
        for i in range(len(speeds_kmh) - 1):
            # Umrechnung von km/h in m/s
            v1_mps = speeds_kmh[i] / 3.6
            v2_mps = speeds_kmh[i+1] / 3.6
            
            p1 = self.points[i+1]
            p2 = self.points[i+2]
            
            t1 = datetime.fromisoformat(p1.time.replace('Z', '+00:00'))
            t2 = datetime.fromisoformat(p2.time.replace('Z', '+00:00'))
            
            dt = (t2 - t1).total_seconds()
            
            if dt > 0:
                accel = (v2_mps - v1_mps) / dt
            else:
                accel = 0.0
                
            accelerations.append(accel)
            
        return accelerations

    def max_acceleration(self):
        """Ermittelt die maximale positive Beschleunigung in m/s²."""
        accels = self.get_accelerations()
        if not accels:
            return 0.0
        return max(accels)
    def get_elevation_data(self):
        """
        Berechnet den Höhenunterschied, die Steigung in % und den Steigungswinkel.
        Gibt eine Liste von Dictionaries mit den Werten für jeden Streckenabschnitt zurück.
        """
        elevation_data = []
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            
            dh = p2.elevation - p1.elevation
            dx = self.haversine_distance(p1, p2)
            
            if dx > 0:
                grad_percent = (dh / dx) * 100
                angle_deg = math.degrees(math.atan2(dh, dx))
            else:
                grad_percent = 0.0
                angle_deg = 0.0
                
            elevation_data.append({
                'dh': dh,
                'gradient_percent': grad_percent,
                'angle_degrees': angle_deg
            })
            
        return elevation_data