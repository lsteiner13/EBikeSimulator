import matplotlib.pyplot as plt
from pathlib import Path


class Plotter:
    """
    Central plotting utility for EBike simulation results.
    X-axis = travelled distance [km]
    """

    # --------------------------------------------------
    # internal helper
    # --------------------------------------------------

    @staticmethod
    def _setup(ax, ylabel: str, file_name: str):

        ax.set_xlabel("Distance [km]")
        ax.set_ylabel(ylabel)
        ax.grid(True)

        projekt_ordner = Path(__file__).resolve().parents[1]
        output_ordner = projekt_ordner / "output"
        output_ordner.mkdir(parents=True, exist_ok=True)

        if not file_name.endswith(".png"):
            file_name += ".png"

        plt.savefig(output_ordner / file_name, dpi=300)
        plt.close()

    # --------------------------------------------------
    # plots
    # --------------------------------------------------

    @staticmethod
    def plot_speed(distance, speed, route_name):

        fig, ax = plt.subplots()
        ax.plot(distance, speed)

        Plotter._setup(
            ax,
            "Speed [m/s]",
            route_name + "_speed"
        )

        return fig

    @staticmethod
    def plot_acceleration(distance, acceleration, route_name):

        fig, ax = plt.subplots()
        ax.plot(distance, acceleration)

        Plotter._setup(
            ax,
            "Acceleration [m/s²]",
            route_name + "_accel"
        )

        return fig

    @staticmethod
    def plot_power(distance, power, route_name):

        fig, ax = plt.subplots()
        ax.plot(distance, power)

        Plotter._setup(
            ax,
            "Power [W]",
            route_name + "_power"
        )

        return fig

    @staticmethod
    def plot_current(distance, current, route_name):

        fig, ax = plt.subplots()
        ax.plot(distance, current)

        Plotter._setup(
            ax,
            "Current [A]",
            route_name + "_current"
        )

        return fig

    @staticmethod
    def plot_voltage(distance, voltage, route_name):

        fig, ax = plt.subplots()
        ax.plot(distance, voltage)

        Plotter._setup(
            ax,
            "Voltage [V]",
            route_name + "_voltage"
        )

        return fig

    @staticmethod
    def plot_soc(distance, soc, route_name):

        fig, ax = plt.subplots()
        ax.plot(distance, soc)

        Plotter._setup(
            ax,
            "State of Charge [%]",
            route_name + "_soc"
        )

        return fig

    @staticmethod
    def plot_batterytemp(distance, batterytemp, route_name):

        fig, ax = plt.subplots()
        ax.plot(distance, batterytemp)

        Plotter._setup(
            ax,
            "Battery temperature [°C]",
            route_name + "_batterytemp"
        )

        return fig

    @staticmethod
    def plot_voltage_current(distance, voltage, current, route_name):

        distance = distance

        fig, ax_v = plt.subplots(figsize=(9, 4.5))
        ax_i = ax_v.twinx()

        ax_v.plot(distance, voltage, "b-", label="Voltage")
        ax_i.plot(distance, current, "r--", label="Current")

        ax_v.set_xlabel("Distance [km]")
        ax_v.set_ylabel("Voltage [V]", color="b")
        ax_i.set_ylabel("Current [A]", color="r")

        ax_v.grid(True)

        fig.legend(loc="upper right")

        return fig

    # --------------------------------------------------
    # plot everything
    # --------------------------------------------------

    @staticmethod
    def plot_all(result, route_name):

        figs = {}

        if hasattr(result, "distance"):

            if hasattr(result, "speed"):
                figs["speed"] = Plotter.plot_speed(
                    result.distance,
                    result.speed,
                    route_name
                )

            if hasattr(result, "power"):
                figs["power"] = Plotter.plot_power(
                    result.distance,
                    result.power,
                    route_name
                )

            if hasattr(result, "current"):
                figs["current"] = Plotter.plot_current(
                    result.distance,
                    result.current,
                    route_name
                )

            if hasattr(result, "voltage"):
                figs["voltage"] = Plotter.plot_voltage(
                    result.distance,
                    result.voltage,
                    route_name
                )

            if hasattr(result, "soc"):
                figs["soc"] = Plotter.plot_soc(
                    result.distance,
                    result.soc,
                    route_name
                )

            if hasattr(result, "battery_temp"):
                figs["batterytemp"] = Plotter.plot_batterytemp(
                    result.distance,
                    result.battery_temp,
                    route_name
                )

        return figs