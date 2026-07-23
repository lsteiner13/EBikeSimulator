from src.physics.route_analyzer import RouteAnalyzer

class SimulationResult:
    """
    Stores the results of a simulation run.
    Each list contains one value per simulation step.
    """

    def __init__(self):
        self.time = []

        self.speed = []
        self.acceleration = []
        self.slope = []

        self.torque = []
        self.power = []
        self.current = []

        self.voltage = []
        self.soc = []

        self.battery_temp = []
        self.distance = []

class Simulator:

    def __init__(self, route):
        self.route = route
        self.analyzer = RouteAnalyzer(route)

    def run(self, bike):

        result = SimulationResult()

        speeds = self.analyzer.get_speeds()
        elevation = self.analyzer.get_elevation_data()
        total_distance = 0.0

        for i in range(len(speeds)):

            speed = speeds[i] / 3.6
            slope = elevation[i]["gradient_percent"] / 100.0
            bike_heading = self.route.points[i].heading
            wind_direction = self.route.points[i].wind_direction
            wind_speed = self.route.points[i].wind_speed
            ambient_temperature = self.route.points[i].temperature
            

            dt = (
                self.route.points[i + 1].time
                - self.route.points[i].time
            ).total_seconds()


            current_elevation = self.route.points[i].elevation
            state = bike.step(speed, slope, dt, bike_heading, wind_direction, wind_speed, ambient_temperature, current_elevation)

            total_distance += state.distance / 1000.0

            result.time.append(self.route.points[i].time)

            result.speed.append(speed)
            result.slope.append(slope)

            result.torque.append(state.torque)
            result.power.append(state.power)
            result.current.append(state.current)
            result.soc.append(state.soc)
            result.voltage.append(state.voltage)
            result.battery_temp.append(state.battery_temp)
            result.distance.append(total_distance)

        return result
    
    def get_summary(self, result: SimulationResult) -> dict:
        #retunrs summary of route + bike

        """Gibt eine vollständige zusammenfassende Statistik der Route + Bike zurück"""
        route_stats = self.analyzer.get_summary()
        soc_start = result.soc[0]
        soc_ende = result.soc[-1]

        battery_v_start = result.voltage[0]
        battery_v_ende = result.voltage[-1]

        battery_temp_start = result.battery_temp[0]
        battery_temp_ende = result.battery_temp[-1]

        highest_power = max(result.power)
        highest_battery_temp = max(result.battery_temp)

        bike_stats = {'soc_start': soc_start,
                     'soc_ende': soc_ende,
                     'battery_v_start': battery_v_start,
                     'battery_v_ende': battery_v_ende,
                     'battery_temp_start': battery_temp_start,
                     'battery_temp_ende': battery_temp_ende,
                     'highest_power': highest_power,
                     'highest_battery_temp': highest_battery_temp
        }

        return route_stats | bike_stats