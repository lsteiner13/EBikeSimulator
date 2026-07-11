import os
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate_txt_report(filepath: str, stats: dict) -> str:
        """
        Generiert einen strukturierten Text-Report aus dem GUI-Stats-Dictionary.
        """
        # Zielverzeichnis erstellen, falls es noch nicht existiert
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        # Report schreiben
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("               E-BIKE SIMULATIONS-REPORT               \n")
            f.write(f"Erstellt am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("1. ROUTEN- UND STRECKENPROFILE\n")
            f.write("-" * 30 + "\n")
            f.write(f"Gesamtdistanz:          {(stats.get('total_distance_m', 0) / 1000):.2f} km\n")
            f.write(f"Höhenmeter (Aufstieg):  {stats.get('total_ascent_m', 0):.0f} m\n")
            f.write(f"Simulierte Fahrzeit:    {round(stats.get('total_duration_s', 0) / 60)} min\n")
            f.write(f"Durchschnittsgeschw.:   {stats.get('average_speed_kmh', 0):.1f} km/h\n")
            f.write("\n")
            
            f.write("2. ENERGIE- & AKKUBILANZ\n")
            f.write("-" * 30 + "\n")
            f.write(f"Start-Akkustand (SoC):  {stats.get('soc_start', 0) * 100:.0f} %\n")
            f.write(f"End-Akkustand (SoC):    {stats.get('soc_ende', 0) * 100:.0f} %\n")
            f.write(f"Max. Akkutemperatur:    {stats.get('highest_battery_temp', 0):.1f} °C\n")
            f.write("\n")
            
            f.write("3. LEISTUNGSANALYSE\n")
            f.write("-" * 30 + "\n")
            f.write(f"Spitzenleistung:        {stats.get('highest_power', 0):.0f} W\n")
            f.write("=" * 60 + "\n")
            
        return filepath