import math
import pandas as pd

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """Berechnet die Distanz zwischen zwei Punkten in Metern."""
    R = 6371000.0
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0)**2
        
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

def calculate_total_distance(df):
    """
    Geht iterativ durch einen DataFrame und summiert die 
    Distanz zwischen den einzelnen GPS-Punkten auf.
    Erwartet Spaltennamen 'lat' und 'lon'.
    """
    total_distance = 0.0
    
    # Schleife durch alle Zeilen bis zur vorletzten
    for i in range(len(df) - 1):
        lat1 = df.iloc[i]['lat']
        lon1 = df.iloc[i]['lon']
        lat2 = df.iloc[i+1]['lat']
        lon2 = df.iloc[i+1]['lon']
        
        distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
        total_distance += distance
        
    return total_distance