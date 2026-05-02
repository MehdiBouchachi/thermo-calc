# thermocalc/app/repositories/batiment_repo.py
"""
Repository for Batiment (Building) database operations.
Handles all SQL queries related to building data.
"""

from mysql.connector import Error


def get_all_batiments(conn):
    """
    Fetch all buildings with zone information.
    
    Args:
        conn: Active database connection.
    
    Returns:
        List of dictionaries containing building data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT b.*, z.nom_zone, r.classe_energetique, r.consommation_kwh
        FROM batiment b
        LEFT JOIN zone_climatique z ON b.id_zone_climatique = z.id
        LEFT JOIN resultat_calcul r ON b.id = r.id_batiment
        ORDER BY b.date_creation DESC
    """)
    return cur.fetchall()


def get_batiment_by_id(conn, batiment_id):
    """
    Fetch a single building by ID.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building to fetch.
    
    Returns:
        Dictionary with building data, or None if not found.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT b.*, z.nom_zone FROM batiment b
        LEFT JOIN zone_climatique z ON b.id_zone_climatique = z.id
        WHERE b.id = %s
    """, (batiment_id,))
    return cur.fetchone()


def insert_batiment(conn, data):
    """
    Insert a new building record.
    
    Args:
        conn: Active database connection.
        data: Dictionary containing batiment fields.
    
    Returns:
        ID of the inserted building (lastrowid).
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        INSERT INTO batiment (code_batiment, adresse_batiment, coordonnees_geo,
            type_batiment, surface, volume, annee_construction,
            nombre_niveaux, nombre_occupants, id_zone_climatique)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get('code_batiment'),
        data.get('adresse_batiment'),
        data.get('coordonnees_geo', ''),
        data.get('type_batiment'),
        float(data.get('surface', 0)),
        float(data.get('volume', 0)) if data.get('volume') else None,
        int(data.get('annee_construction')) if data.get('annee_construction') else None,
        int(data.get('nombre_niveaux', 1)),
        int(data.get('nombre_occupants', 0)),
        int(data.get('id_zone_climatique')) if data.get('id_zone_climatique') else None
    ))
    return cur.lastrowid


def delete_batiment(conn, batiment_id):
    """
    Delete a building by ID.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building to delete.
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM batiment WHERE id = %s", (batiment_id,))


def add_source_energy(conn, batiment_id, source_id):
    """
    Associate an energy source with a building.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
        source_id: ID of the energy source.
    """
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO batiment_source (id_batiment, id_source) VALUES (%s, %s)",
        (batiment_id, source_id)
    )


def get_zones(conn):
    """
    Fetch all climate zones.
    
    Args:
        conn: Active database connection.
    
    Returns:
        List of dictionaries with zone data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM zone_climatique ORDER BY nom_zone")
    return cur.fetchall()


def get_sources(conn):
    """
    Fetch all energy sources.
    
    Args:
        conn: Active database connection.
    
    Returns:
        List of dictionaries with energy source data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM source_energie ORDER BY nom_source")
    return cur.fetchall()
