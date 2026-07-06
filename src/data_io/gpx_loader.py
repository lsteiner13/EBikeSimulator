import gpxpy
from src.models.route import Route, RoutePoint


def load_gpx(path: str) -> Route:
    with open(path, "r") as f:
        gpx = gpxpy.parse(f)

    points = []

    for track in gpx.tracks:
        for segment in track.segments:
            for p in segment.points:
                points.append(
                    RoutePoint(
                        lat=p.latitude,
                        lon=p.longitude,
                        elevation=p.elevation,
                        time=p.time
                    )
                )

    return Route(points)