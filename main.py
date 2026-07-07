import logging
import sys
from src.data_io.csv_loader import load_csv
from src.data_io.gpx_loader import load_gpx
from pathlib import Path
from src.models.bike import EBike, EBikeConfig
from src.models.motor import Motor
from src.models.battery import LiPo, NMC
from src.physics.route_analyzer import RouteAnalyzer
from src.simulator.simulator import Simulator
from tools.plot_gps_data import FoliumMap
from tools.plotter import Plotter

# Logging Basis-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

# Pfad zur Datendatei
data_path = Path(__file__).resolve().parents[0] / "data" / "final_project_input_data.csv"

if not data_path.exists():
    logging.critical(f"Daten-Datei nicht gefunden: {data_path}")
    sys.exit(1)

# --- 1. Exception Handling beim Laden der Daten ---
try:
    logging.info("Lade Route aus CSV...")
    route = load_csv(data_path)
    logging.info(f"Route erfolgreich geladen.")
except Exception as e:
    logging.critical(f"Fehler beim Laden der CSV-Datei: {e}")
    sys.exit(1)

# --- 2. Exception Handling & PLausabilitätsprüfung bei der Konfiguration ---
try:
    logging.info("Initialisiere E-Bike Komponenten...")
    
    # init motor
    motor = Motor(efficiency=0.85, torque_constant=1.5)
    
    # init batterys
    lipo = LiPo(capacity_cell_Ah=10, s_parallel=4, initial_soc=1)
    nmc = NMC(capacity_cell_Ah=10, s_parallel=4, initial_soc=1)
    
    ebike_config = EBikeConfig(mass=80, wheel_diameter=27, c_w_a=0.5626, rolling_resistance=0.006)
    
    # init ebike versions
    ebike_lipo = EBike(motor=motor, battery=lipo, config=ebike_config)
    ebike_nmc = EBike(motor=motor, battery=nmc, config=ebike_config)
    
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

FoliumMap.plot_route(route)
Plotter.plot_speed(result_lipo.time, result_lipo.speed)
Plotter.plot_power(result_lipo.time, result_lipo.power)
Plotter.plot_soc(result_lipo.time, result_lipo.soc)

logging.info("Alle Prozesse fehlerfrei beendet.")
