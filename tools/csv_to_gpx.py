import pandas as pd
import gpxpy
import gpxpy.gpx
import argparse

def csv_to_gpx(csv_path: str, gpx_path: str):

    # CSV einlesen
    df = pd.read_csv(csv_path, sep=";")

    # GPX-Datei erstellen
    gpx = gpxpy.gpx.GPX()

    # Track anlegen
    track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(track)

    # Segment anlegen
    segment = gpxpy.gpx.GPXTrackSegment()
    track.segments.append(segment)

    # Punkte hinzufügen
    for _, row in df.iterrows():
        point = gpxpy.gpx.GPXTrackPoint(
            latitude=row["lat"],
            longitude=row["lon"],
            elevation=row["ele"],
            time=pd.to_datetime(row["time"])
        )
        segment.points.append(point)

    # GPX speichern
    with open(gpx_path, "w", encoding="utf-8") as f:
        f.write(gpx.to_xml())

    print("GPX-Datei erfolgreich erstellt.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")

    args = parser.parse_args()

    csv_to_gpx(args.input, args.output)