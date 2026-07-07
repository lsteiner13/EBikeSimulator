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

class Simulator:

    def __init__(self, route):
        self.route = route
        self.analyzer = RouteAnalyzer(route)

    def run(self, bike):

        result = SimulationResult()

        speeds = self.analyzer.get_speeds()
        elevation = self.analyzer.get_elevation_data()

        for i in range(len(speeds)):

            speed = speeds[i] / 3.6
            slope = elevation[i]["gradient_percent"] / 100.0
            bike_heading = self.route.points[i].heading
            wind_direction = self.route.points[i].wind_direction
            wind_speed = self.route.points[i].wind_speed

            dt = (
                self.route.points[i + 1].time
                - self.route.points[i].time
            ).total_seconds()

            state = bike.step(speed, slope, dt, bike_heading, wind_direction, wind_speed)

            result.time.append(self.route.points[i].time)

            result.speed.append(speed)
            result.slope.append(slope)

            result.torque.append(state.torque)
            result.power.append(state.power)
            result.current.append(state.current)
            result.soc.append(state.soc)
            result.voltage.append(state.voltage)

        return result