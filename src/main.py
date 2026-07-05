from data_io.csv_loader import load_csv
from pathlib import Path
from models.bike import EBike, EBikeConfig
from models.motor import Motor
from models.battery import LiPo
from physics.route_analyzer import RouteAnalyzer  # Neu importiert für den Analyzer

# aktuelles File: .../src/main.py
# 1 pfad nach oben
data_path = Path(__file__).resolve().parents[1] / "data" / "final_project_input_data.csv"

if not data_path.exists():
    raise FileNotFoundError(f"File not found: {data_path}")

# load route
route = load_csv(data_path)

# RouteAnalyzer mit der geladenen Route instanziieren
analyzer = RouteAnalyzer(route)

motor = Motor(efficiency=0.85, torque_constant=1.5)
lipo = LiPo(capacity_cell_Ah=10, s_parallel=10, initial_soc=1)
ebike_config = EBikeConfig(mass=70, wheel_diameter=27, c_w_a=0.5626)

ebike = EBike(motor=motor, battery=lipo, config=ebike_config)

# Daten aus dem Analyzer holen
speeds = analyzer.get_speeds()
elevation_data = analyzer.get_elevation_data()

max_power_seen = 0.0

for i in range(len(speeds)):
    
    current_speed = speeds[i] / 3.6
    
    current_slope = elevation_data[i]['gradient_percent'] / 100.0
    
    air_drag = ebike.air_drag(current_speed)
    slope_force = ebike.slope_force(current_slope)
    needed_torque = ebike.required_torque(current_speed, current_slope)
    needed_power = ebike.required_power(current_speed, current_slope)
    
    if needed_power > max_power_seen:
        max_power_seen = needed_power

# --- Einzelner Testschritt (Physik-Check) ---
test_speed = 10 #10m/s
test_slope = 0.05 #5%
dt = 5 #sekunden

print("--- Einzel-Testschritt ---")
print(f"Air drag: {ebike.air_drag(test_speed)}")
print(f"Slope force: {ebike.slope_force(test_slope)}")
print(f"Needed torque: {ebike.required_torque(test_speed, test_slope)}")
print(f"Needed power: {ebike.required_power(test_speed, test_slope)}")
print(f"Simulate one step: {ebike.step(test_speed, test_slope, dt)}\n")
print(f"Maximale benötigte Leistung auf der gesamten Route: {max_power_seen:.2f} W")