# thermocalc/app/repositories/ouvrant_repo.py
"""
Repository for Ouvrant (Window/Opening) database operations.
Handles SQL queries for window component management.
"""


def get_openings_by_batiment(conn, batiment_id):
    """
    Fetch all windows/openings for a building.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
    
    Returns:
        List of dictionaries containing opening data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT o.*, to2.nom_type, to2.k_ouvrant FROM ouvrant o
        JOIN type_ouvrant to2 ON o.id_type_ouvrant = to2.id
        WHERE o.id_batiment = %s ORDER BY o.numero_ouvrant
    """, (batiment_id,))
    return cur.fetchall()


def get_next_opening_number(conn, batiment_id):
    """
    Get the next opening number for a building.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
    
    Returns:
        Next opening number (integer).
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT COUNT(*) as cnt FROM ouvrant WHERE id_batiment = %s",
        (batiment_id,)
    )
    return cur.fetchone()['cnt'] + 1


def insert_opening(conn, batiment_id, numero, surface, condition, type_id, deperdition):
    """
    Insert a new opening record.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
        numero: Opening number.
        surface: Surface area in m².
        condition: Condition of the opening.
        type_id: ID of the opening type.
        deperdition: Heat loss value in W/K.
    """
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ouvrant (id_batiment, numero_ouvrant, surface_ouvrant,
                            etat_ouvrant, id_type_ouvrant, deperdition_ouvrant)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (batiment_id, numero, surface, condition, type_id, deperdition))


def get_opening_type_k(conn, type_id):
    """
    Get the thermal transmission coefficient for an opening type.
    
    Args:
        conn: Active database connection.
        type_id: ID of the opening type.
    
    Returns:
        Thermal transmission coefficient as float.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT k_ouvrant FROM type_ouvrant WHERE id = %s", (type_id,))
    result = cur.fetchone()
    return float(result['k_ouvrant']) if result else 0.0


def get_all_opening_types(conn):
    """
    Fetch all opening types.
    
    Args:
        conn: Active database connection.
    
    Returns:
        List of dictionaries with opening type data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM type_ouvrant")
    return cur.fetchall()
