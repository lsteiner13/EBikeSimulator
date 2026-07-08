from dataclasses import dataclass

from src.models.motor import Motor
from src.models.battery import BatteryBase

import math

@dataclass
class EBikeConfig:
    mass: float
    wheel_diameter: float
    c_w_a: float
    rolling_resistance: float

    def __post_init__(self):
        # Plausibilitätsprüfungen direkt nach der Initialisierung
        if self.mass <= 0:
            raise ValueError(f"Ungültige Masse: {self.mass} kg. Die Gesamtmasse muss größer als 0 sein.")
        
        if self.wheel_diameter <= 0:
            raise ValueError(f"Ungültiger Raddurchmesser: {self.wheel_diameter} inch. Muss größer als 0 sein.")
        
        if self.c_w_a < 0:
            raise ValueError(f"Ungültiger Luftwiderstandsbeiwert: {self.c_w_a}. Darf nicht negativ sein.")
        
        if self.rolling_resistance <= 0:
            raise ValueError(f"Ungültiger Rolwiderstand: {self.rolling_resistance}. Darf nicht negativ sein.")

@dataclass
class StepResult:
    torque: float
    omega: float
    power: float
    current: float
    voltage: float
    soc: float
    battery_temp: float


class EBike:
    """
    EBike class - now combines all parts, motor, battery, bike config
    include function to calculate 
    """

    def __init__(self, motor: Motor, battery: BatteryBase, config: EBikeConfig):
        self.motor = motor
        self.battery = battery
        self.config = config

    def air_drag(self, velocity: float, wind_speed: float) -> float:
        """formel
        Fw = 1/2 * luftdichte * cw * A * v²
        c_w_a -> cw * A
        nehme standart wert für luftdichte
        luftdichte auf meeres höhe bei 15° ~ 1,225kg / m³
        berücksichtige wind -> berechne relative geschwindigkeit
        wind_speed wird bereits korrekt übergeben 
        + -> rückenwind
        - -> gegenwind"""
        air_density = 1.225
        rel_speed = velocity - wind_speed

        return 0.5 * air_density * self.config.c_w_a * rel_speed**2
    
    def wind_component(self, bike_heading, wind_direction, wind_speed):
        """
        Gibt Windkomponente in Fahrtrichtung zurück.
        Positiv = Rückenwind
        Negativ = Gegenwind
        """

        angle = math.radians(
            wind_direction - bike_heading
        )

        return wind_speed * math.cos(angle)

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
    
    def rolling_resistance(self, slope: float = 0.0) -> float:
        #formel für reibung = rollreibung * m * g * cos(alpha)
        #aus steigung winkel berechnen -> alpha = atan(steigung) 
        alpha = math.atan(slope)
        
        return self.config.rolling_resistance * self.config.mass * 9.81 * math.cos(alpha)
        
    def required_power(self, velocity: float, slope: float):
        """
        Total power on wheel
        Formula = P = F * v
        """
        F_air = self.air_drag(velocity)
        F_slope = self.slope_force(slope)
        F_rolling_resistance = self.rolling_resistance(slope)

        total_force = F_air + F_slope + F_rolling_resistance

        return total_force * velocity

    def required_torque(self, velocity: float, slope: float, wind_speed: float):
        """"
        Formula = τ = F*r 
        """
        F_air = self.air_drag(velocity, wind_speed)
        F_slope = self.slope_force(slope)
        F_rolling_resistance = self.rolling_resistance(slope)
 
        conversion_factor_inch_to_m = 0.0254

        total_force = F_air + F_slope + F_rolling_resistance

        return total_force * self.config.wheel_diameter/2 * conversion_factor_inch_to_m


    def step(self, velocity: float, slope: float, dt: float, bike_heading: float, wind_direction: float, wind_speed: float, ambient_temperature: float) -> StepResult:
        """
        One time step in simulation
        """
        rel_wind_speed = self.wind_component(bike_heading, wind_direction, wind_speed)
        torque = self.required_torque(velocity, slope, rel_wind_speed)
        omega = self.wheel_omega(velocity)

        # mechanische Leistung
        mech_power = torque * omega

        # Current
        current = self.motor.torque_to_current(torque)

        # Akku entladen
        self.battery.apply_current(current, dt)

        # Akku Temperaturänderung berechnen
        self.battery.update_temperature(current, ambient_temperature, dt)

        return StepResult(
            torque=torque,
            omega=omega,
            power=mech_power,
            current=current,
            voltage=self.battery.voltage(current),
            soc=self.battery.soc,
            battery_temp=self.battery.temperature,
)