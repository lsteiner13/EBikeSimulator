import os
from datetime import datetime
from fpdf import FPDF

class ReportGenerator:
    @staticmethod
    def generate_txt_report(filepath: str, stats: dict) -> str:
        """Generiert einen strukturierten Text-Report aus dem GUI-Stats-Dictionary."""
        if not filepath.endswith('.txt'):
            filepath = filepath.split('.')[0] + '.txt'
            
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("                 E-BIKE SIMULATIONS-REPORT                 \n")
            f.write(f"Erstellt am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("1. ROUTEN- UND STRECKENPROFILE\n")
            f.write("-" * 30 + "\n")
            f.write(f"Gesamtdistanz:         {(stats.get('total_distance_m', 0) / 1000):.2f} km\n")
            f.write(f"Hoehenmeter (Aufstieg): {stats.get('total_ascent_m', 0):.0f} m\n")
            f.write(f"Simulierte Fahrzeit:   {round(stats.get('total_duration_s', 0) / 60)} min\n")
            f.write(f"Durchschnittsgeschw.:  {stats.get('average_speed_kmh', 0):.1f} km/h\n\n")
            
            f.write("2. ENERGIE- & AKKUBILANZ\n")
            f.write("-" * 30 + "\n")
            f.write(f"Start-Akkustand (SoC):  {stats.get('soc_start', 0) * 100:.0f} %\n")
            f.write(f"End-Akkustand (SoC):    {stats.get('soc_ende', 0) * 100:.0f} %\n")
            f.write(f"Max. Akkutemperatur:   {stats.get('highest_battery_temp', 0):.1f} °C\n\n")
            
            f.write("3. LEISTUNGSANALYSE\n")
            f.write("-" * 30 + "\n")
            f.write(f"Spitzenleistung:       {stats.get('highest_power', 0):.0f} W\n")
            f.write("=" * 60 + "\n")
            
        return filepath

    @staticmethod
    def generate_pdf_report(filepath: str, stats: dict) -> str:
        """Generiert einen formatierten PDF-Report aus dem GUI-Stats-Dictionary."""
        # Sicherstellen, dass die Dateiendung stimmt
        if not filepath.endswith('.pdf'):
            filepath = filepath.split('.')[0] + '.pdf'
            
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        # PDF-Dokument initialisieren (A4, Maßeinheit mm)
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_margins(15, 15, 15)
        
        # Kopfzeile / Titel
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "E-BIKE SIMULATIONS-REPORT", ln=True, align="C")
        pdf.set_font("Arial", "I", 9)
        pdf.cell(0, 6, f"Erstellt am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        pdf.ln(10)
        
        # Sektion 1: Route
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "1. ROUTEN- UND STRECKENPROFILE", ln=True)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y()) # Trennlinie
        pdf.ln(3)
        
        pdf.set_font("Arial", "", 10)
        dist = stats.get('total_distance_m', 0) / 1000
        ascent = stats.get('total_ascent_m', 0)
        duration = round(stats.get('total_duration_s', 0) / 60)
        avg_speed = stats.get('average_speed_kmh', 0)
        
        pdf.cell(60, 6, "Gesamtdistanz:", border=0)
        pdf.cell(0, 6, f"{dist:.2f} km", ln=True)
        pdf.cell(60, 6, "Hoehenmeter (Aufstieg):", border=0)
        pdf.cell(0, 6, f"{ascent:.0f} m", ln=True)
        pdf.cell(60, 6, "Simulierte Fahrzeit:", border=0)
        pdf.cell(0, 6, f"{duration} min", ln=True)
        pdf.cell(60, 6, "Durchschnittsgeschw.:", border=0)
        pdf.cell(0, 6, f"{avg_speed:.1f} km/h", ln=True)
        pdf.ln(6)
        
        # Sektion 2: Batterie
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "2. ENERGIE- & AKKUBILANZ", ln=True)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(3)
        
        pdf.set_font("Arial", "", 10)
        soc_start = stats.get('soc_start', 0) * 100
        soc_ende = stats.get('soc_ende', 0) * 100
        max_temp = stats.get('highest_battery_temp', 0)
        
        pdf.cell(60, 6, "Start-Akkustand (SoC):", border=0)
        pdf.cell(0, 6, f"{soc_start:.0f} %", ln=True)
        pdf.cell(60, 6, "End-Akkustand (SoC):", border=0)
        pdf.cell(0, 6, f"{soc_ende:.0f} %", ln=True)
        pdf.cell(60, 6, "Max. Akkutemperatur:", border=0)
        pdf.cell(0, 6, f"{max_temp:.1f} Grad C", ln=True)
        pdf.ln(6)
        
        # Sektion 3: Leistung
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "3. LEISTUNGSANALYSE", ln=True)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(3)
        
        pdf.set_font("Arial", "", 10)
        highest_power = stats.get('highest_power', 0)
        
        pdf.cell(60, 6, "Spitzenleistung:", border=0)
        pdf.cell(0, 6, f"{highest_power:.0f} W", ln=True)
        
        # Datei speichern
        pdf.output(filepath)
        return filepath