# thermocalc/app/models/composants.py
"""
Data models for building components (walls, floors, roofs, windows).
Defines structures for all heat loss-contributing building elements.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Mur:
    """Wall component model."""
    id: int
    id_batiment: int
    numero_mur: int
    longueur_mur: float
    hauteur_mur: float
    etat_mur: str
    id_type_mur: int
    deperdition_mur: float
    nom_type: Optional[str] = None
    k_mur: Optional[float] = None


@dataclass
class Plancher:
    """Floor component model."""
    id: int
    id_batiment: int
    numero_plancher: int
    etat_plancher: str
    surface_plancher: float
    id_type_plancher: int
    deperdition_plancher: float
    nom_type: Optional[str] = None
    k_plancher: Optional[float] = None


@dataclass
class Toiture:
    """Roof component model."""
    id: int
    id_batiment: int
    numero_toiture: int
    etat_toiture: str
    surface_toit: float
    id_type_toiture: int
    deperdition_toiture: float
    nom_type: Optional[str] = None
    k_toiture: Optional[float] = None


@dataclass
class Ouvrant:
    """Window/opening component model."""
    id: int
    id_batiment: int
    numero_ouvrant: int
    surface_ouvrant: float
    etat_ouvrant: str
    id_type_ouvrant: int
    deperdition_ouvrant: float
    nom_type: Optional[str] = None
    k_ouvrant: Optional[float] = None
