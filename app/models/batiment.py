# thermocalc/app/models/batiment.py
"""
Data models for Batiment (Building) entity.
Defines the structure of building objects using dataclasses.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Batiment:
    """
    Represents a building (bâtiment) in the thermal calculation system.
    
    Attributes:
        id: Unique building identifier.
        code_batiment: Unique building code (e.g., 'BAT-001').
        adresse_batiment: Physical address of the building.
        coordonnees_geo: Geographic coordinates (latitude, longitude).
        type_batiment: Type of building (e.g., 'Bureau', 'Hôpital').
        surface: Total surface area in m².
        volume: Total volume in m³, optional.
        annee_construction: Year the building was constructed.
        nombre_niveaux: Number of floors/levels.
        nombre_occupants: Number of occupants.
        id_zone_climatique: Reference to climate zone.
        date_creation: Timestamp when record was created.
        nom_zone: Name of the climate zone (joined from zone_climatique table).
    """
    
    id: int
    code_batiment: str
    adresse_batiment: str
    type_batiment: str
    surface: float
    nombre_niveaux: int
    nombre_occupants: int
    id_zone_climatique: Optional[int] = None
    coordonnees_geo: Optional[str] = None
    volume: Optional[float] = None
    annee_construction: Optional[int] = None
    date_creation: Optional[datetime] = None
    nom_zone: Optional[str] = None
