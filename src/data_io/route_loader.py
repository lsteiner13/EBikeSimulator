from pathlib import Path

from src.data_io.csv_loader import load_csv
from src.data_io.gpx_loader import load_gpx
from src.data_io.weather_loader import WeatherLoader

def load_route_file(file_path: Path):
    """
    Loads a route file depending on its extension.
    Supports CSV and GPX.
    """

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix == ".csv":
        route = load_csv(file_path)

    elif suffix == ".gpx":
        route = load_gpx(file_path)

    else:
        raise ValueError(
            f"Unsupported file format: {suffix}. "
            "Supported formats are .csv and .gpx"
        )
    
    #add weathherdata
    WeatherLoader.adder(route)

    return route