import matplotlib.pyplot as plt

class Plotter:
    """
    Central plotting utility for EBike simulation results.
    Expects time-series data: time + value arrays.
    """

    # ---------------------------
    # internal helper
    # ---------------------------
    @staticmethod
    def _setup(ax, xlabel: str, ylabel: str):
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        plt.show()

    # ---------------------------
    # basic plots
    # ---------------------------
    @staticmethod
    def plot_speed(time, speed):
        fig, ax = plt.subplots()
        ax.plot(time, speed)
        Plotter._setup(ax, "Time [s]", "Speed [m/s]")
        return fig

    @staticmethod
    def plot_acceleration(time, acceleration):
        fig, ax = plt.subplots()
        ax.plot(time, acceleration)
        Plotter._setup(ax, "Time [s]", "Acceleration [m/s²]")
        return fig

    @staticmethod
    def plot_power(time, power):
        fig, ax = plt.subplots()
        ax.plot(time, power)
        Plotter._setup(ax, "Time [s]", "Power [W]")
        return fig

    @staticmethod
    def plot_current(time, current):
        fig, ax = plt.subplots()
        ax.plot(time, current)
        Plotter._setup(ax, "Time [s]", "Current [A]")
        return fig

    @staticmethod
    def plot_voltage(time, voltage):
        fig, ax = plt.subplots()
        ax.plot(time, voltage)
        Plotter._setup(ax, "Time [s]", "Voltage [V]")
        return fig

    @staticmethod
    def plot_soc(time, soc):
        fig, ax = plt.subplots()
        ax.plot(time, soc)
        Plotter._setup(ax, "Time [s]", "State of Charge [-]")
        return fig
    
    @staticmethod
    def plot_voltage_current(time, voltage, current):
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
    def plot_all(result):
        """
        Expects a SimulationResult object.
        """

        figs = {}

        if hasattr(result, "time"):

            if hasattr(result, "speed"):
                figs["speed"] = Plotter.plot_speed(result.time, result.speed)

            if hasattr(result, "power"):
                figs["power"] = Plotter.plot_power(result.time, result.power)

            if hasattr(result, "current"):
                figs["current"] = Plotter.plot_current(result.time, result.current)

            if hasattr(result, "voltage"):
                figs["voltage"] = Plotter.plot_voltage(result.time, result.voltage)

            if hasattr(result, "soc"):
                figs["soc"] = Plotter.plot_soc(result.time, result.soc)

        return figs