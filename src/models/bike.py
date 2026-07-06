from dataclasses import dataclass

from src.models.motor import Motor
from src.models.battery import BatteryBase

@dataclass
class EBikeConfig:
    mass: float                 # Gesamtmasse (Bike + Fahrer) in kg
    wheel_diameter: float        # in inch
    c_w_a: float               # Luftwiderstandsfläche

@dataclass
class StepResult:
    torque: float
    omega: float
    power: float
    current: float
    voltage: float
    soc: float


class EBike:
    """
    EBike class - now combines all parts, motor, battery, bike config
    include function to calculate 
    """

    def __init__(self, motor: Motor, battery: BatteryBase, config: EBikeConfig):
        self.motor = motor
        self.battery = battery
        self.config = config

    def air_drag(self, velocity: float):
        """formel
        Fw = 1/2 * luftdichte * cw * A * v²
        c_w_a -> cw * A
        nehme standart wert für luftdichte
        luftdichte auf meeres höhe bei 15° ~ 1,225kg / m³"""
        air_density = 1.225

        return 0.5 * air_density * self.config.c_w_a * velocity**2

    def slope_force(self, slope: float):
        """Hangabtriebskraft - muss zusätzlich überwunden werden 
        #Formel -> m*g * steigung 
        #Steigung (slope) wird erwartet mit delta h / delta s
        """
        return self.config.mass * 9.81 * slope
    
    def wheel_omega(self, velocity: float):
        """ω = v / r
        wheel diameter in inch (gets converted to meter)"""
        conversion_factor_inch_to_m = 0.0254
        return velocity / (self.config.wheel_diameter/2 * conversion_factor_inch_to_m)

    def required_power(self, velocity: float, slope: float):
        """
        Total power on wheel
        Formula = P = F * v
        """
        F_air = self.air_drag(velocity)
        F_slope = self.slope_force(slope)

        total_force = F_air + F_slope

        return total_force * velocity

    def required_torque(self, velocity: float, slope: float):
        """"
        Formula = τ = F*r 
        """
        F_air = self.air_drag(velocity)
        F_slope = self.slope_force(slope)
        conversion_factor_inch_to_m = 0.0254

        total_force = F_air + F_slope

        return total_force * self.config.wheel_diameter/2 * conversion_factor_inch_to_m


    def step(self, velocity: float, slope: float, dt: float):
        """
        One time step in simulation
        """

        torque = self.required_torque(velocity, slope)
        omega = self.wheel_omega(velocity)

        # mechanische Leistung
        mech_power = torque * omega

        # Current
        current = self.motor.torque_to_current(torque)

        # Akku entladen
        self.battery.apply_current(current, dt)

        return StepResult(
            torque=torque,
            omega=omega,
            power=mech_power,
            current=current,
            voltage=self.battery.voltage(current),
            soc=self.battery.soc,
)