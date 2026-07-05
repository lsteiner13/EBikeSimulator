import pandas as pd
from models.route import Route, RoutePoint


def load_csv(path: str) -> Route:
    df = pd.read_csv(path, sep=";")

    points = [
        RoutePoint(
            lat=row["lat"],
            lon=row["lon"],
            elevation=row["ele"],
            time=pd.to_datetime(row["time"])
        )
        for _, row in df.iterrows()
    ]

    return Route(points)