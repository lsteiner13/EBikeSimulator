import pandas as pd
import os

def load_gps_data(file_path):
    """
    Liest GPS-Daten aus der angegeben CSV-Datei in einen Pandas DataFrame ein.
    Enthält eine grundlegende Fehlerbehandlung.
    """
    if not os.path.exists(file_path):
        print(f"Fehler: Die Datei '{file_path}' wurde nicht gefunden.")
        return None
    
    try:
        df = pd.read_csv(file_path)
        print(f"Daten erfolgreich geladen. Anzahl der Zeilen: {len(df)}")
        return df
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return None

if __name__ == "__main__":
    # Ermittelt den Ordner, in dem dieses Skript liegt (src)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Baut den Pfad zusammen: Gehe vom src-Ordner eins hoch (..) und dann in data
    path_to_csv = os.path.join(script_dir, "..", "data", "final_project_input_data.csv")
    
    # Funktion aufrufen
    gps_data = load_gps_data(path_to_csv)
    
    # Ausgabe der ersten 5 Zeilen zur Kontrolle
    if gps_data is not None:
        print(gps_data.head())