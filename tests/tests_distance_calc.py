import unittest
import pandas as pd
import sys
import os

# Pfad anpassen, damit Python die Datei im src-Ordner findet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# HIER ANGEPASST: Importiert jetzt aus distance_calc
from distance_calc import calculate_haversine_distance, calculate_total_distance

class TestDistanceCalculator(unittest.TestCase):

    def test_haversine_distance(self):
        # Test: Innsbruck bis München (Luftlinie)
        # Erwarteter Wert: ca. 97.700 Meter
        dist = calculate_haversine_distance(47.2682, 11.3933, 48.1371, 11.5754)
        
        # assertAlmostEqual erlaubt eine kleine Abweichung (delta) bei Floats
        self.assertAlmostEqual(dist, 97700, delta=1000)

    def test_total_distance(self):
        # Wir simulieren einen kleinen DataFrame mit 3 Punkten
        test_data = {
            'lat': [47.2682, 47.5000, 48.1371], 
            'lon': [11.3933, 11.4500, 11.5754]
        }
        df = pd.DataFrame(test_data)
        
        # Funktion aufrufen
        total = calculate_total_distance(df)
        
        # Die Strecke über 3 Punkte muss logischerweise berechnet werden
        # Wir prüfen, ob ein sinnvoller Wert herauskommt
        self.assertTrue(total > 0)
        self.assertIsInstance(total, float)

if __name__ == '__main__':
    unittest.main()