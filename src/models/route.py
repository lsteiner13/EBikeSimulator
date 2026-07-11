from dataclasses import dataclass
from datetime import datetime

@dataclass
class RoutePoint:
    lat: float
    lon: float
    elevation: float
    time: datetime
    
    heading: float = None
    temperature: float = None
    wind_speed: float = None
    wind_direction: float = None
    

class Route:
    def __init__(self, points: list[RoutePoint]):
        self._validate_points(points)
        self.points = points

    def _validate_points(self, points: list[RoutePoint]):
        for index, p in enumerate(points):
            if not (-90.0 <= p.lat <= 90.0):
                raise ValueError(f"Fehler bei Punkt {index}: Breitengrad {p.lat} ist ungültig. Erlaubt: -90 bis 90.")
            if not (-180.0 <= p.lon <= 180.0):
                raise ValueError(f"Fehler bei Punkt {index}: Längengrad {p.lon} ist ungültig. Erlaubt: -180 bis 180.")

    def __len__(self):
        return len(self.points)

    def __iter__(self):
        return iter(self.points)

    def __str__(self):
        return f"Route mit {len(self.points)} validierten Punkten"