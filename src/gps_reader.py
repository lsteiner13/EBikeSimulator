import pandas as pd
import os

def load_gps_data(file_path):
    """
    Liest GPS-Daten ein und validiert die geforderten Akzeptanzkriterien.
    """
    if not os.path.exists(file_path):
        print(f"Fehler: Die Datei '{file_path}' wurde nicht gefunden.")
        return None
    
    try:
        # sep=';' ist zwingend notwendig, da eure CSV Semikolons nutzt
        df = pd.read_csv(file_path, sep=';')
        
        # Die exakten Spaltennamen aus eurer Datei
        required_columns = ['time', 'lat', 'lon', 'ele']
        
        # Überprüfen, ob alle geforderten Spalten existieren
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Fehler bei der Validierung: Fehlende Spalten {missing_columns}")
            return None
            
        print("Daten erfolgreich geladen und validiert.")
        print("Verfügbar: Zeitstempel (time), Latitude (lat), Longitude (lon), Höhe (ele).")
        print(f"Anzahl der Datenpunkte (Zeilen): {len(df)}")
        return df
        
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return None

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_csv = os.path.join(script_dir, "..", "data", "final_project_input_data.csv")
    
    gps_data = load_gps_data(path_to_csv)
    if gps_data is not None:
        print("\nDie ersten 5 Zeilen zur Kontrolle:")
        print(gps_data.head())