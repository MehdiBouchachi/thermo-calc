"""Building service for building management operations."""

from app.repositories import (batiment_repo, mur_repo, plancher_repo, toiture_repo,
                               ouvrant_repo, resultat_repo)


def get_all(conn) -> list[dict]:
    """Returns all batiments as raw dicts (for index listing)."""
    return batiment_repo.find_all(conn)


def get_detail(conn, batiment_id: int) -> dict | None:
    """
    Returns a full detail dict for one batiment including all composants,
    resultat, and form type lists. Returns None if not found.
    """
    row = batiment_repo.find_by_id(conn, batiment_id)
    if not row:
        return None
    return {
        'batiment': row,
        'murs': mur_repo.find_by_batiment(conn, batiment_id),
        'planchers': plancher_repo.find_by_batiment(conn, batiment_id),
        'toitures': toiture_repo.find_by_batiment(conn, batiment_id),
        'ouvrants': ouvrant_repo.find_by_batiment(conn, batiment_id),
        'resultat': resultat_repo.find_by_batiment(conn, batiment_id),
        'types_mur': mur_repo.find_all_types(conn),
        'types_plancher': plancher_repo.find_all_types(conn),
        'types_toiture': toiture_repo.find_all_types(conn),
        'types_ouvrant': ouvrant_repo.find_all_types(conn),
    }


def create(conn, form_data: dict, source_ids: list) -> int:
    """Inserts a batiment and its energy sources. Returns new batiment id."""
    batiment_id = batiment_repo.insert(conn, form_data)
    batiment_repo.insert_sources(conn, batiment_id, source_ids)
    return batiment_id


def delete(conn, batiment_id: int) -> None:
    """Deletes a batiment and all its composants (cascades via FK)."""
    batiment_repo.delete(conn, batiment_id)


def get_form_data(conn) -> dict:
    """Returns zones and sources needed to render the creation form."""
    return {
        'zones': batiment_repo.find_all_zones(conn),
        'sources': batiment_repo.find_all_sources(conn),
    }
