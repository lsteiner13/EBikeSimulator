import math
from datetime import datetime
from src.models.route import Route  

class RouteAnalyzer:
    def __init__(self, route: Route):  
        self.route = route
        self.points = route.points

        #calculate headings
        self.calculate_headings()

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
        """Berechnet die Geschwindigkeiten (in km/h) zwischen den Wegpunkten."""
        speeds_kmh = []
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            
            # Distanz in Metern (Haversine)
            dist_m = self.haversine_distance(p1, p2)
            
            # Zeitdifferenz in Sekunden
            dt_s = (p2.time - p1.time).total_seconds()
            
            if dt_s > 0:
                speed_ms = dist_m / dt_s
                speeds_kmh.append(speed_ms * 3.6)
            else:
                speeds_kmh.append(0.0) # Fallback, falls Zeitdifferenz = 0
                
        return speeds_kmh

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
            
            dt = (p2.time - p1.time).total_seconds()
            
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
    
    def total_ascent(self) -> float:
        """Berechnet die gesamten Höhenmeter im Aufstieg (kumulierter positiver Höhenunterschied)."""
        elevation_data = self.get_elevation_data()
        return float(sum(section['dh'] for section in elevation_data if section['dh'] > 0))

    def total_descent(self) -> float:
        """Berechnet die gesamten Höhenmeter im Abstieg (kumulierter negativer Höhenunterschied)."""
        elevation_data = self.get_elevation_data()
        # Wir nehmen den Absolutwert (abs), damit der Wert positiv ausgegeben wird
        return float(sum(abs(section['dh']) for section in elevation_data if section['dh'] < 0))

    def get_total_duration_seconds(self) -> float:
        """Berechnet die Gesamtfahrzeit in Sekunden basierend auf den Zeitstempeln der Punkte."""
        if len(self.points) < 2:
            return 0.0
        duration = self.points[-1].time - self.points[0].time
        return float(duration.total_seconds())

    def get_summary(self) -> dict:
        """Gibt eine vollständige zusammenfassende Statistik der Route zurück."""
        speeds = self.get_speeds()
        accelerations = self.get_accelerations()
        elevation_data = self.get_elevation_data()
        
        avg_speed = sum(speeds) / len(speeds) if speeds else 0.0
        max_speed = max(speeds) if speeds else 0.0
        max_accel = max(accelerations) if accelerations else 0.0
        max_gradient = max([sec['gradient_percent'] for sec in elevation_data]) if elevation_data else 0.0
        
        return {
            'total_distance_m': self.total_distance(),
            'total_duration_s': self.get_total_duration_seconds(),
            'average_speed_kmh': avg_speed,
            'max_speed_kmh': max_speed,
            'max_acceleration_mps2': max_accel,
            'total_ascent_m': self.total_ascent(),
            'total_descent_m': self.total_descent(),
            'max_gradient_percent': max_gradient,
            'start_time': self.points[0].time, 
            'end_time': self.points[-1].time
        }
    
    @staticmethod
    def calculate_heading(p1, p2):
        """
        Berechnet Fahrtrichtung zwischen zwei GPS Punkten.
        Ergebnis in Grad:
        0 = Nord
        90 = Ost
        180 = Süd
        270 = West
        """

        lat1 = math.radians(p1.lat)
        lat2 = math.radians(p2.lat)

        delta_lon = math.radians(
            p2.lon - p1.lon
        )

        x = math.sin(delta_lon) * math.cos(lat2)

        y = (
            math.cos(lat1) * math.sin(lat2)
            -
            math.sin(lat1)
            * math.cos(lat2)
            * math.cos(delta_lon)
        )

        heading = math.atan2(x, y)

        heading = math.degrees(heading)

        return (heading + 360) % 360

    def calculate_headings(self):

        points = self.route.points

        for i in range(len(points)-1):

            points[i].heading = (
                self.calculate_heading(
                    points[i],
                    points[i+1]
                )
            )

        # letzter Punkt übernimmt Richtung vom vorherige
        points[-1].heading = points[-2].heading