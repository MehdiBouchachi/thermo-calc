# thermocalc/app/models/resultat.py
"""
Data model for calculation results.
Represents thermal calculation outcomes for a building.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ResultatCalcul:
    """
    Represents thermal calculation results for a building.
    
    Attributes:
        id: Unique result identifier.
        id_batiment: Reference to the building.
        deperdition_totale: Total heat loss in W/K.
        consommation_kwh: Annual energy consumption in kWh/m²/an.
        classe_energetique: Energy class (A-G).
        date_calcul: Timestamp when calculation was performed.
    """
    
    id: int
    id_batiment: int
    deperdition_totale: float
    consommation_kwh: float
    classe_energetique: str
    date_calcul: Optional[datetime] = None
