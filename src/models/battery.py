from abc import ABC, abstractmethod
from models.ocv_curves import OCV_CURVES
from scipy.interpolate import interp1d

class BatteryBase(ABC):
    @abstractmethod
    def __init__(self, capacity_nom_Ah: float, initial_soc: float = 1.0):
        self.C_nom = capacity_nom_Ah * 3600.0  # Kapazität in As
        self.soc = initial_soc
        self.R_int = 0.08
        self.Vmin = 32.0
        self.Vmax = 42.0

    @abstractmethod
    def apply_current(self, current: float, duration: float) -> None:
        pass

    @abstractmethod
    def voltage(self, current: float = 0.0) -> float:
        pass

class BatteryPack(BatteryBase):
    """
    Simple model of a battery pack as a single cell.
    The battery is modeled as an ideal voltage source (open circuit voltage) in series with an internal resistance.
    The open circuit voltage is a linear function of the state of charge (SoC).
    The SoC is updated based on the applied current and duration.
    """

    def __init__(
        self,
        capacity_nom_Ah: float,
        internal_resistance_mOhm: float = 80.0,
        initial_soc: float = 1.0,
        Vmin: float = 3.0,
        Vmax: float = 4.2,
    ):
        self.capacity_nom_As = capacity_nom_Ah*3600
        self.internal_resistance_Ohm = internal_resistance_mOhm/1000
        self.soc = initial_soc
        self.Vmin = Vmin
        self.Vmax = Vmax
        

    def apply_current(self, current: float, duration: float) -> None:
        """Modify the SoC based on the applied current & duration"""
        self.soc = max(0, min(1, self.soc - (current * duration) / self.capacity_nom_As))

    def is_empty(self) -> bool:
        return self.soc <= 0.0

    def is_full(self) -> bool:
        return self.soc >= 1.0

    def voltage(self, current: float = 0.0) -> float:
        """Return the current voltage of the battery at the SoC and the given current flow"""
        return self.Vmin + max(0, self.soc*(self.Vmax-self.Vmin) - self.internal_resistance_Ohm*current)

    def __str__(self):
        return f"BatteryPack(SoC={self.soc * 100:.1f}%, V={self.voltage():.2f} V)"
    

class LiPo(BatteryPack): 
    """
    LiPo battery details:
    10SxP (10 cells in series, x cells paralell)
    nominal voltage: 3.7V per cell
    minimal voltage: 3.2V per cell
    maximal voltage: 4.2V per cell
    internal resistance: 8mΩ per cell

    define new init for additional parameter needed 
    *cell para amount
    *init base class with calculated values (series cell add voltage, para cell add capacity)

    use ocv curve to get more accurate results
    """

    def __init__(
        self,
        capacity_cell_Ah: float,
        s_parallel: int = 1,
        internal_resistance_cell_mOhm: float = 8.0,
        initial_soc: float = 1.0,
    ):
        self.s_series = 10
        self.s_parallel = s_parallel

        # Gesamtkapazität
        capacity_pack_Ah = capacity_cell_Ah * s_parallel

        # Gesamtenergie in As
        super().__init__(
            capacity_nom_Ah=capacity_pack_Ah,
            internal_resistance_mOhm=internal_resistance_cell_mOhm * self.s_series / self.s_parallel,
            initial_soc=initial_soc,
            Vmin=self.s_series * 3.2,
            Vmax=self.s_series * 4.2,
        )

        # OCV-Kennlinie
        curve = OCV_CURVES["lipo"]
        self.ocv_func = interp1d(
            curve["soc"],
            curve["voc"],
            kind="linear",
            fill_value="extrapolate"
        )

    def voltage(self, current: float = 0.0) -> float:
        """
        LiPo-specific voltage model using OCV curve + internal resistance
        """

        u_oc = float(self.ocv_func(self.soc))
        u_term = u_oc - self.internal_resistance_Ohm * current

        return max(0.0, u_term)
    
    def __str__(self):
        return f"LiPo(SoC={self.soc * 100:.1f}%, V={self.voltage():.2f} V)"
    
class NMC(BatteryPack): 
    """
    NMC battery details:
    10SxP (10 cells in series, x cells paralell)
    nominal voltage: 3.7V per cell
    minimal voltage: 3.2V per cell
    maximal voltage: 4.2V per cell
    internal resistance: 7mΩ per cell

    define new init for additional parameter needed 
    *cell para amount
    *init base class with calculated values (series cell add voltage, para cell add capacity)

    use ocv curve to get more accurate results
    """

    def __init__(
        self,
        capacity_cell_Ah: float,
        s_parallel: int = 1,
        internal_resistance_cell_mOhm: float = 7.0,
        initial_soc: float = 1.0,
    ):
        self.s_series = 10
        self.s_parallel = s_parallel

        # Gesamtkapazität
        capacity_pack_Ah = capacity_cell_Ah * s_parallel

        # Gesamtenergie in As
        super().__init__(
            capacity_nom_Ah=capacity_pack_Ah,
            internal_resistance_mOhm=internal_resistance_cell_mOhm * self.s_series / self.s_parallel,
            initial_soc=initial_soc,
            Vmin=self.s_series * 3.2,
            Vmax=self.s_series * 4.2,
        )

        # OCV-Kennlinie
        curve = OCV_CURVES["nmc"]
        self.ocv_func = interp1d(
            curve["soc"],
            curve["voc"],
            kind="linear",
            fill_value="extrapolate"
        )

    def voltage(self, current: float = 0.0) -> float:
        """
        Nmc-specific voltage model using OCV curve + internal resistance
        """

        u_oc = float(self.ocv_func(self.soc))
        u_term = u_oc - self.internal_resistance_Ohm * current

        return max(0.0, u_term)
    
    def __str__(self):
        return f"NMC(SoC={self.soc * 100:.1f}%, V={self.voltage():.2f} V)"
    
if __name__ == "__main__":
    """
    Simple test cases when run as main
    """
    battery = BatteryPack(capacity_nom_Ah=10, initial_soc=0.7, Vmin=32.0, Vmax=42.0)
    print(battery)

    battery.apply_current(current=5.0, duration=300.0)
    print(battery)
    battery.apply_current(current=10.0, duration=240.0)
    print(battery)
    battery.apply_current(current=-5.0, duration=150.0)

    print(battery)

    #Test case for lipo
    lipo = LiPo(capacity_cell_Ah=10, initial_soc=0.7)
    print(lipo)

    lipo.apply_current(current=5.0, duration=300.0)
    print(lipo)
    lipo.apply_current(current=50.0, duration=240.0)
    print(lipo)
    lipo.apply_current(current=-5.0, duration=150.0)

    print(lipo)

    #Test case for nmc
    nmc = NMC(capacity_cell_Ah=10, initial_soc=0.7)
    print(nmc)

    nmc.apply_current(current=5.0, duration=300.0)
    print(nmc)
    nmc.apply_current(current=50.0, duration=240.0)
    print(nmc)
    nmc.apply_current(current=-5.0, duration=150.0)

    print(nmc)