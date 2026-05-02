# thermocalc/app/services/batiment_service.py
"""
Building management service.
Handles business logic for building creation, retrieval, and deletion.
"""

from app.repositories import batiment_repo, mur_repo, plancher_repo, toiture_repo, ouvrant_repo


def get_all_buildings(conn):
    """
    Retrieve all buildings with their energy information.
    
    Args:
        conn: Active database connection.
    
    Returns:
        List of building dictionaries.
    """
    return batiment_repo.get_all_batiments(conn)


def get_building_details(conn, batiment_id):
    """
    Retrieve detailed information for a single building including all components.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
    
    Returns:
        Dictionary with building data and component lists, or None if not found.
    """
    batiment = batiment_repo.get_batiment_by_id(conn, batiment_id)
    if not batiment:
        return None
    
    return {
        'batiment': batiment,
        'murs': mur_repo.get_walls_by_batiment(conn, batiment_id),
        'planchers': plancher_repo.get_floors_by_batiment(conn, batiment_id),
        'toitures': toiture_repo.get_roofs_by_batiment(conn, batiment_id),
        'ouvrants': ouvrant_repo.get_openings_by_batiment(conn, batiment_id),
        'types_mur': mur_repo.get_all_wall_types(conn),
        'types_plancher': plancher_repo.get_all_floor_types(conn),
        'types_toiture': toiture_repo.get_all_roof_types(conn),
        'types_ouvrant': ouvrant_repo.get_all_opening_types(conn),
    }


def create_building(conn, form_data):
    """
    Create a new building record with associated energy sources.
    
    Args:
        conn: Active database connection.
        form_data: Dictionary with building information from form submission.
    
    Returns:
        ID of the created building.
    """
    batiment_id = batiment_repo.insert_batiment(conn, form_data)
    
    # Add energy sources if provided
    sources = form_data.getlist('sources') if hasattr(form_data, 'getlist') else []
    for source_id in sources:
        batiment_repo.add_source_energy(conn, batiment_id, source_id)
    
    return batiment_id


def delete_building(conn, batiment_id):
    """
    Delete a building and all associated data.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building to delete.
    """
    batiment_repo.delete_batiment(conn, batiment_id)


def get_form_options(conn):
    """
    Get all options needed for the building creation form.
    
    Args:
        conn: Active database connection.
    
    Returns:
        Dictionary with zones and energy sources.
    """
    return {
        'zones': batiment_repo.get_zones(conn),
        'sources': batiment_repo.get_sources(conn),
    }
