from pathlib import Path
import webbrowser

import folium

class FoliumMap:

    @staticmethod
    def plot_route(route, output_file="route_map.html", open_browser=True):
        """
        Creates an interactive OpenStreetMap with the GPS route.
        """

        if not route.points:
            raise ValueError("Route contains no points.")

        start = route.points[0]

        m = folium.Map(
            location=[start.lat, start.lon],
            zoom_start=13,
            tiles=None
        )

        folium.TileLayer(
            "OpenTopoMap",
            name="Topographic"
        ).add_to(m)

        folium.TileLayer(
            "CartoDB Positron",
            name="Light Map"
        ).add_to(m)

        folium.LayerControl().add_to(m)

        coords = [(p.lat, p.lon) for p in route.points]

        # Route
        folium.PolyLine(
            coords,
            color="blue",
            weight=4,
            opacity=0.8
        ).add_to(m)

        # Start marker
        folium.Marker(
            coords[0],
            popup="Start",
            icon=folium.Icon(color="green")
        ).add_to(m)

        # End marker
        folium.Marker(
            coords[-1],
            popup="End",
            icon=folium.Icon(color="red")
        ).add_to(m)

        output = Path(output_file)
        m.save(output)

        print(f"Map saved to {output.resolve()}")

        if open_browser:
            webbrowser.open(output.resolve().as_uri())