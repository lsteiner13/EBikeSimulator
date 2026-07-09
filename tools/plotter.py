import matplotlib.pyplot as plt
from pathlib import Path

class Plotter:
    """
    Central plotting utility for EBike simulation results.
    Expects time-series data: time + value arrays.
    """

    # ---------------------------
    # internal helper
    # ---------------------------
    @staticmethod
    def _setup(ax, xlabel: str, ylabel: str, file_name: str) -> None:
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        dateiname = file_name
        projekt_ordner = Path(__file__).resolve().parents[1]
        output_ordner = projekt_ordner / "output"
        output_ordner.mkdir(parents=True, exist_ok=True)
        if not dateiname.endswith(".png"):
            dateiname += ".png"

        ziel_pfad = output_ordner / dateiname

        plt.savefig(ziel_pfad, dpi=300)

        #close plt
        plt.close()
    # ---------------------------
    # basic plots
    # ---------------------------
    @staticmethod
    def plot_speed(time, speed, route_name):
        fig, ax = plt.subplots()
        ax.plot(time, speed)
        Plotter._setup(ax, "Time [s]", "Speed [m/s]", route_name + "_speed")
        return fig

    @staticmethod
    def plot_acceleration(time, acceleration, route_name):
        fig, ax = plt.subplots()
        ax.plot(time, acceleration)
        Plotter._setup(ax, "Time [s]", "Acceleration [m/s²]", route_name + "_accel")
        return fig

    @staticmethod
    def plot_power(time, power, route_name):
        fig, ax = plt.subplots()
        ax.plot(time, power)
        Plotter._setup(ax, "Time [s]", "Power [W]", route_name + "_power")
        return fig

    @staticmethod
    def plot_current(time, current, route_name):
        fig, ax = plt.subplots()
        ax.plot(time, current)
        Plotter._setup(ax, "Time [s]", "Current [A]", route_name + "_current")
        return fig

    @staticmethod
    def plot_voltage(time, voltage, route_name):
        fig, ax = plt.subplots()
        ax.plot(time, voltage)
        Plotter._setup(ax, "Time [s]", "Voltage [V]", route_name + "_voltage")
        return fig

    @staticmethod
    def plot_soc(time, soc, route_name):
        fig, ax = plt.subplots()
        ax.plot(time, soc)
        Plotter._setup(ax, "Time [s]", "State of Charge [-]", route_name + "_soc")
        return fig

    @staticmethod
    def plot_batterytemp(time, batterytemp, route_name):
        fig, ax = plt.subplots()
        ax.plot(time, batterytemp)
        Plotter._setup(ax, "Time [s]", "Battery temperature [°C]", route_name + "_batterytemp")
        return fig
    
    @staticmethod
    def plot_voltage_current(time, voltage, current, route_name):
        fig, ax_v = plt.subplots(figsize=(9, 4.5))
        ax_i = ax_v.twinx()

        ax_v.plot(time, voltage, "b-", label="Voltage [V]")
        ax_i.plot(time, current, "r--", label="Current [A]")

        ax_v.set_xlabel("Time [s]")
        ax_v.set_ylabel("Voltage [V]", color="b")
        ax_i.set_ylabel("Current [A]", color="r")

        ax_v.grid(True)

        fig.legend(loc="upper right")
        return fig

    @staticmethod
    def plot_all(result, route_name):
        """
        Expects a SimulationResult object.
        """

        figs = {}

        if hasattr(result, "time"):

            if hasattr(result, "speed"):
                figs["speed"] = Plotter.plot_speed(result.time, result.speed, route_name)

            if hasattr(result, "power"):
                figs["power"] = Plotter.plot_power(result.time, result.power, route_name)

            if hasattr(result, "current"):
                figs["current"] = Plotter.plot_current(result.time, result.current, route_name)

            if hasattr(result, "voltage"):
                figs["voltage"] = Plotter.plot_voltage(result.time, result.voltage, route_name)

            if hasattr(result, "soc"):
                figs["soc"] = Plotter.plot_soc(result.time, result.soc, route_name)

            if hasattr(result, "battery_temp"):
                figs["batterytemp"] = Plotter.plot_batterytemp(result.time, result.battery_temp, route_name)

        return figs