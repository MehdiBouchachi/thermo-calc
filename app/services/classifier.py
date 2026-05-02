# thermocalc/app/services/classifier.py
"""
Energy classification service for thermal calculations.
Assigns DPE energy classes (A-G) based on consumption values.
"""


def classify(consommation):
    """
    Classify a building's energy efficiency based on annual consumption.
    
    Classification follows the DPE (Diagnostic de Performance Énergétique) standard:
    - A: ≤ 70 kWh/m²/an (Best)
    - B: ≤ 110 kWh/m²/an
    - C: ≤ 180 kWh/m²/an
    - D: ≤ 250 kWh/m²/an
    - E: ≤ 330 kWh/m²/an
    - F: ≤ 420 kWh/m²/an
    - G: > 420 kWh/m²/an (Worst)
    
    Args:
        consommation: Annual energy consumption in kWh/m²/an.
    
    Returns:
        Energy class as single character string (A-G).
    """
    if consommation <= 70:
        return 'A'
    elif consommation <= 110:
        return 'B'
    elif consommation <= 180:
        return 'C'
    elif consommation <= 250:
        return 'D'
    elif consommation <= 330:
        return 'E'
    elif consommation <= 420:
        return 'F'
    else:
        return 'G'
