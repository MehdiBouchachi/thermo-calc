# thermocalc/app/services/calcul_service.py
"""
Thermal calculation service.
Handles computation of building heat loss and energy consumption.
"""

from app.repositories import resultat_repo, mur_repo, plancher_repo, toiture_repo, ouvrant_repo
from app.repositories import batiment_repo
from app.services.classifier import classify


def compute_deperdition(conn, batiment_id):
    """
    Compute total heat loss and energy consumption for a building.
    
    Formula: consumption = (total_deperdition * 2400) / (surface * 1000)
    where 2400 is estimated annual heating hours.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building to calculate.
    
    Returns:
        Dictionary with calculation results including:
        - dep_murs: Wall heat loss
        - dep_planchers: Floor heat loss
        - dep_toitures: Roof heat loss
        - dep_ouvrants: Opening heat loss
        - dep_totale: Total heat loss
        - consommation: Energy consumption in kWh/m²/an
        - classe: Energy class (A-G)
    """
    
    # Get building surface
    batiment = batiment_repo.get_batiment_by_id(conn, batiment_id)
    if not batiment:
        raise ValueError(f"Building {batiment_id} not found")
    
    surface = float(batiment['surface'])
    
    # Sum deperditions from each component type
    dep_murs = resultat_repo.sum_deperditions(conn, batiment_id, 'mur')
    dep_planchers = resultat_repo.sum_deperditions(conn, batiment_id, 'plancher')
    dep_toitures = resultat_repo.sum_deperditions(conn, batiment_id, 'toiture')
    dep_ouvrants = resultat_repo.sum_deperditions(conn, batiment_id, 'ouvrant')
    
    dep_totale = dep_murs + dep_planchers + dep_toitures + dep_ouvrants
    
    # Calculate consumption: (W/K * 2400h/year) / (surface * 1000)
    consommation = (dep_totale * 2400) / (surface * 1000) if surface > 0 else 0
    
    # Classify energy efficiency
    classe = classify(consommation)
    
    # Persist results
    resultat_repo.insert_or_update_result(
        conn, batiment_id, 
        round(dep_totale, 3),
        round(consommation, 3),
        classe
    )
    
    return {
        'dep_murs': round(dep_murs, 3),
        'dep_planchers': round(dep_planchers, 3),
        'dep_toitures': round(dep_toitures, 3),
        'dep_ouvrants': round(dep_ouvrants, 3),
        'dep_totale': round(dep_totale, 3),
        'consommation': round(consommation, 3),
        'classe': classe
    }


def add_wall_component(conn, batiment_id, type_id, length, height, condition):
    """
    Add a wall component to a building and calculate its heat loss.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
        type_id: ID of the wall type.
        length: Wall length in meters.
        height: Wall height in meters.
        condition: Condition description (e.g., 'Bon état').
    
    Returns:
        Dictionary with deperdition value and surface.
    """
    k = mur_repo.get_wall_type_k(conn, type_id)
    surface = float(length) * float(height)
    deperdition = float(k) * surface
    
    numero = mur_repo.get_next_wall_number(conn, batiment_id)
    mur_repo.insert_wall(conn, batiment_id, numero, length, height, condition, type_id, deperdition)
    
    return {
        'deperdition': round(deperdition, 3),
        'surface': round(surface, 2)
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
