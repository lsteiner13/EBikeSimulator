from dataclasses import dataclass
from datetime import datetime


@dataclass
class RoutePoint:
    lat: float
    lon: float
    elevation: float
    time: datetime

class Route:
    def __init__(self, points: list[RoutePoint]):
        self.points = points

    def __len__(self):
        return len(self.points)

    def __iter__(self):
        return iter(self.points)
    
    def __str__(self):
        return f"{self.points}"