from data_io.csv_loader import load_csv
from pathlib import Path
from models.bike import EBike, EBikeConfig
from models.motor import Motor
from models.battery import LiPo

# aktuelles File: .../src/main.py
# 1 pfad nach oben
data_path = Path(__file__).resolve().parents[1] / "data" / "final_project_input_data.csv"

if not data_path.exists():
    raise FileNotFoundError(f"File not found: {data_path}")

#load route
route = load_csv(data_path)

motor = Motor(efficiency=0.85, torque_constant=1.5)
lipo = LiPo(capacity_cell_Ah=10, s_parallel=10, initial_soc=1)
ebike_config = EBikeConfig(mass=70, wheel_diameter=27, c_w_a=0.5626)

ebike = EBike(motor=motor, battery=lipo, config=ebike_config)

test_speed = 10 #10m/s
test_slope = 0.05 #5%
dt = 5 #sekunden
#test air drag


print(f"Air drag: {ebike.air_drag(test_speed)}")
print(f"Slope force: {ebike.slope_force(test_slope)}")
print(f"Needed torque: {ebike.required_torque(test_speed, test_slope)}")
print(f"Needed power: {ebike.required_power(test_speed, test_slope)}")
print(f"Simulate one step: {ebike.step(test_speed, test_slope, dt)}")