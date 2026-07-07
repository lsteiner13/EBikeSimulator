import unittest
import sys
import os

# Pfad zum Projekt-Hauptverzeichnis (EBikeSimulator) hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports an die aktuelle Architektur anpassen
from src.models.bike import EBike, EBikeConfig
from src.models.motor import Motor
from src.models.battery import LiPo

class TestPhysics(unittest.TestCase):
    
    def setUp(self):
        self.motor = Motor(efficiency=0.85, torque_constant=1.5)
        self.battery = LiPo(capacity_cell_Ah=10, s_parallel=4, initial_soc=1.0)
        self.config = EBikeConfig(mass=80, wheel_diameter=27, c_w_a=0.5626)
        self.ebike = EBike(motor=self.motor, battery=self.battery, config=self.config)

    def test_leistung(self):
        # 1. Test: Fahren in der Ebene 
        power_flat = self.ebike.required_power(velocity=10.0, slope=0.0)
        self.assertTrue(power_flat > 0, "Leistung in der Ebene muss > 0 sein (Luftwiderstand).")

        # 2. Test: Bergauf 
        power_uphill = self.ebike.required_power(velocity=10.0, slope=0.05)
        self.assertTrue(power_uphill > power_flat, "Bergauf muss mehr Leistung kosten als in der Ebene.")

        # 3. Test: Stark bergab 
        power_downhill = self.ebike.required_power(velocity=10.0, slope=-0.10)
        self.assertTrue(power_downhill < 0, "Bei starkem Gefälle muss die mechanische Leistung negativ sein.")

    def test_akku(self):
        # 1. Test: Startzustand prüfen
        self.assertEqual(self.battery.soc, 1.0, "Akku sollte mit 100 % (1.0) starten.")

        # 2. Test: Normales Entladen 
        self.battery.apply_current(current=10.0, duration=360.0)
        self.assertTrue(self.battery.soc < 1.0, "SoC muss nach Stromentnahme sinken.")

        # 3. Test: Überladen verhindern 
        self.battery.apply_current(current=-1000.0, duration=3600.0) 
        self.assertEqual(self.battery.soc, 1.0, "SoC darf durch Rekuperation nicht über 1.0 steigen.")

        # 4. Test: Tiefenentladung verhindern
        self.battery.apply_current(current=1000.0, duration=36000.0) 
        self.assertEqual(self.battery.soc, 0.0, "SoC darf beim Leersaugen nicht unter 0.0 fallen.")

if __name__ == '__main__':
    unittest.main()