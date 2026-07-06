from src.data_io.csv_loader import load_csv
from pathlib import Path
from src.models.bike import EBike, EBikeConfig
from src.models.motor import Motor
from src.models.battery import LiPo
from src.models.battery import NMC
from src.physics.route_analyzer import RouteAnalyzer
from src.simulator.simulator import Simulator

# aktuelles File: .../src/main.py
# 1 pfad nach oben
data_path = Path(__file__).resolve().parents[0] / "data" / "final_project_input_data.csv"

if not data_path.exists():
    raise FileNotFoundError(f"File not found: {data_path}")

# load route
route = load_csv(data_path)

#init motor
motor = Motor(efficiency=0.85, torque_constant=1.5)

#init batterys
lipo = LiPo(capacity_cell_Ah=10, s_parallel=4, initial_soc=1)
nmc = NMC(capacity_cell_Ah=10, s_parallel=4, initial_soc=1)

#ebike config
ebike_config = EBikeConfig(mass=80, wheel_diameter=27, c_w_a=0.5626)

#init ebike versions
ebike_lipo = EBike(motor=motor, battery=lipo, config=ebike_config)
ebike_nmc = EBike(motor=motor, battery=nmc, config=ebike_config)

#load route in simulator
simulator = Simulator(route)

#simulate with ebike lipo and nmc
result_lipo = simulator.run(ebike_lipo)
result_nmc = simulator.run(ebike_nmc)