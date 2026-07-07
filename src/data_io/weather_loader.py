from datetime import datetime, timezone
import requests


class WeatherLoader:

    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"


    @staticmethod
    def load_day(latitude, longitude, day):

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": day.strftime("%Y-%m-%d"),
            "end_date": day.strftime("%Y-%m-%d"),
            "hourly": (
                "temperature_2m,"
                "wind_speed_10m,"
                "wind_direction_10m"
            ),
            "wind_speed_unit": "ms",
            "timezone": "UTC",
        }

        response = requests.get(
            WeatherLoader.BASE_URL,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        return response.json()


    @staticmethod
    def interpolate(value1, value2, factor):
        """
        Lineare Interpolation

        factor:
        0.0 -> value1
        1.0 -> value2
        """

        return value1 + factor * (value2 - value1)


    @staticmethod
    def adder(route):

        if not route.points:
            return


        cache = {}


        for point in route.points:

            day = point.time.date()


            if day not in cache:

                cache[day] = WeatherLoader.load_day(
                    point.lat,
                    point.lon,
                    day
                )


            data = cache[day]


            times = [
                datetime.fromisoformat(t).replace(tzinfo=timezone.utc)
                for t in data["hourly"]["time"]
            ]


            before = None
            after = None


            for i in range(len(times)-1):

                if times[i] <= point.time <= times[i+1]:
                    before = i
                    after = i + 1
                    break

            if point.time < times[0] or point.time > times[-1]:
                raise ValueError(
                    "Route time outside weather data range"
                )

            total_seconds = (
                times[after] - times[before]
            ).total_seconds()


            passed_seconds = (
                point.time - times[before]
            ).total_seconds()


            factor = passed_seconds / total_seconds


            point.temperature = WeatherLoader.interpolate(
                data["hourly"]["temperature_2m"][before],
                data["hourly"]["temperature_2m"][after],
                factor
            )


            point.wind_speed = WeatherLoader.interpolate(
                data["hourly"]["wind_speed_10m"][before],
                data["hourly"]["wind_speed_10m"][after],
                factor
            )


            point.wind_direction = WeatherLoader.interpolate(
                data["hourly"]["wind_direction_10m"][before],
                data["hourly"]["wind_direction_10m"][after],
                factor
            )