import logging
import sys
from src.data_io.route_loader import load_route_file
from pathlib import Path
from src.models.bike import EBike, EBikeConfig
from src.models.motor import Motor
from src.models.battery import LiPo, NMC
from src.physics.route_analyzer import RouteAnalyzer
from src.simulator.simulator import Simulator
from tools.plot_gps_data import FoliumMap
from tools.plotter import Plotter
import argparse

# Parser erstellen
parser = argparse.ArgumentParser(description="EBike Simulatoins Software")

# Optional route file
parser.add_argument("--route_file", type=str, default=str(Path(__file__).resolve().parents[0] / "data" / "final_project_input_data.csv"), help="Pfad zur Routendatei (Standard /data/final_project_input_data.csv)")

# Optional soc
parser.add_argument("--soc", type=float, default=1, help="Start-Akkustand in Flieskomma 0-1 (Standard: 1)")

# Optional weight
parser.add_argument("--weight", type=float, default=85, help="Gewicht in kg (Standard 85kg)")

#optional rider power
parser.add_argument("--rpower", type=float, default=50, help="Unterstützung des Fahrers beim Fahren des E-Bike (Standard 50W)")

# Argumente parsen
args = parser.parse_args()

# Zugriff auf die Werte
route_path = args.route_file
start_soc = args.soc
start_weight = args.weight
rider_power = args.rpower

# Logging Basis-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

# Pfad zur Datendatei
data_path = Path(route_path)

if not data_path.exists():
    logging.critical(f"Daten-Datei nicht gefunden: {data_path}")
    sys.exit(1)

# --- 1. Exception Handling beim Laden der Daten ---
try:
    logging.info("Lade Route aus Datei...")
    route = load_route_file(data_path)
    logging.info(f"Route erfolgreich geladen.")
except Exception as e:
    logging.critical(f"Fehler beim Laden der Datei: {e}")
    sys.exit(1)

# --- 2. Exception Handling & PLausabilitätsprüfung bei der Konfiguration ---
try:
    logging.info("Initialisiere E-Bike Komponenten...")
    
    # init motor
    motor = Motor(efficiency=0.85, torque_constant=1.5)
    
    # init batterys
    lipo = LiPo(capacity_cell_Ah=4, s_parallel=4, initial_soc=start_soc, initial_temperature=route.points[0].temperature)
    nmc = NMC(capacity_cell_Ah=4, s_parallel=4, initial_soc=start_soc, initial_temperature=route.points[0].temperature)
    
    ebike_config = EBikeConfig(mass=start_weight, wheel_diameter=27, c_w_a=0.5626, rolling_resistance=0.006)
    
    # init ebike versions
    ebike_lipo = EBike(motor=motor, battery=lipo, config=ebike_config, rider_power=rider_power)
    ebike_nmc = EBike(motor=motor, battery=nmc, config=ebike_config, rider_power=rider_power)
    
    logging.info("Komponenten erfolgreich initialisiert.")

except ValueError as ve:
    # Fängt gezielt unsere Plausibilitätsprüfungen (zb. negative Masse) ab
    logging.error(f"Konfigurationsfehler: {ve}")
    sys.exit(1)
except Exception as e:
    logging.error(f"Unerwarteter Fehler bei der Initialisierung: {e}")
    sys.exit(1)

# --- 3. Exception Handling während der Simulation ---
try:
    logging.info("Lade Route in den Simulator...")
    simulator = Simulator(route)
    
    logging.info("Starte Simulation für E-Bike mit LiPo-Akku...")
    result_lipo = simulator.run(ebike_lipo)
    logging.info("Simulation (LiPo) erfolgreich abgeschlossen.")
    
    logging.info("Starte Simulation für E-Bike mit NMC-Akku...")
    result_nmc = simulator.run(ebike_nmc)
    logging.info("Simulation (NMC) erfolgreich abgeschlossen.")
    
except Exception as e:
    # Fängt Abstürze ab, falls in der ausgelagerten Simulator-Klasse etwas schiefgeht
    logging.critical(f"Kritischer Fehler während der Simulation: {e}")
    sys.exit(1)

#Plots
route_name = data_path.stem
projekt_ordner = Path(__file__).resolve().parents[0]
output_ordner = projekt_ordner / "output"
output_filename = output_ordner / route_name
str_output_filename = str(output_filename)

Plotter.plot_all(result_lipo, route_name + "_lipo")
Plotter.plot_all(result_nmc, route_name + "_nmc")
FoliumMap.plot_route(route, output_file=str_output_filename + "_map.html", open_browser=False)

logging.info("Alle Prozesse fehlerfrei beendet.")
