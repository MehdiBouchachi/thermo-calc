"""Calculation service for thermal deperdition and consumption."""

from app.repositories import (mur_repo, plancher_repo, toiture_repo, ouvrant_repo,
                               resultat_repo)
from app.models.mur import Mur
from app.models.plancher import Plancher
from app.models.toiture import Toiture
from app.models.ouvrant import Ouvrant
from app.services.classifier import classify


def compute(conn, batiment_id: int, surface: float) -> dict:
    """
    Fetches all composants, builds model objects, calls calculer_deperdition()
    on each (satisfying the teacher's class diagram), persists the result,
    and returns a result dict for the controller.
    """
    murs = [Mur.from_db_row(r) for r in mur_repo.find_by_batiment(conn, batiment_id)]
    planchers = [Plancher.from_db_row(r) for r in plancher_repo.find_by_batiment(conn, batiment_id)]
    toitures = [Toiture.from_db_row(r) for r in toiture_repo.find_by_batiment(conn, batiment_id)]
    ouvrants = [Ouvrant.from_db_row(r) for r in ouvrant_repo.find_by_batiment(conn, batiment_id)]

    dep_murs = round(sum(m.calculer_deperdition() for m in murs), 3)
    dep_planchers = round(sum(p.calculer_deperdition() for p in planchers), 3)
    dep_toitures = round(sum(t.calculer_deperdition() for t in toitures), 3)
    dep_ouvrants = round(sum(o.calculer_deperdition() for o in ouvrants), 3)
    dep_totale = round(dep_murs + dep_planchers + dep_toitures + dep_ouvrants, 3)

    consommation = round((dep_totale * 2400) / (surface * 1000), 3) if surface > 0 else 0
    classe = classify(consommation)

    resultat_repo.upsert(conn, batiment_id, dep_totale, consommation, classe)

    return {
        'dep_murs': dep_murs,
        'dep_planchers': dep_planchers,
        'dep_toitures': dep_toitures,
        'dep_ouvrants': dep_ouvrants,
        'dep_totale': dep_totale,
        'consommation': consommation,
        'classe': classe
    }


def add_floor_component(conn, batiment_id, type_id, surface, condition):
    """
    Add a floor component to a building and calculate its heat loss.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
        type_id: ID of the floor type.
        surface: Floor surface area in m².
        condition: Condition description.
    
    Returns:
        Dictionary with deperdition value.
    """
    k = plancher_repo.get_floor_type_k(conn, type_id)
    deperdition = float(k) * float(surface)
    
    numero = plancher_repo.get_next_floor_number(conn, batiment_id)
    plancher_repo.insert_floor(conn, batiment_id, numero, condition, surface, type_id, deperdition)
    
    return {'deperdition': round(deperdition, 3)}


def add_roof_component(conn, batiment_id, type_id, surface, condition):
    """
    Add a roof component to a building and calculate its heat loss.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
        type_id: ID of the roof type.
        surface: Roof surface area in m².
        condition: Condition description.
    
    Returns:
        Dictionary with deperdition value.
    """
    k = toiture_repo.get_roof_type_k(conn, type_id)
    deperdition = float(k) * float(surface)
    
    numero = toiture_repo.get_next_roof_number(conn, batiment_id)
    toiture_repo.insert_roof(conn, batiment_id, numero, condition, surface, type_id, deperdition)
    
    return {'deperdition': round(deperdition, 3)}


def add_opening_component(conn, batiment_id, type_id, surface, condition):
    """
    Add an opening (window) component to a building and calculate its heat loss.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
        type_id: ID of the opening type.
        surface: Opening surface area in m².
        condition: Condition description.
    
    Returns:
        Dictionary with deperdition value.
    """
    k = ouvrant_repo.get_opening_type_k(conn, type_id)
    deperdition = float(k) * float(surface)
    
    numero = ouvrant_repo.get_next_opening_number(conn, batiment_id)
    ouvrant_repo.insert_opening(conn, batiment_id, numero, surface, condition, type_id, deperdition)
    
    return {'deperdition': round(deperdition, 3)}
