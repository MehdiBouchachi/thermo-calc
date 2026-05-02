# thermocalc/app/repositories/toiture_repo.py
"""
Repository for Toiture (Roof) database operations.
Handles SQL queries for roof component management.
"""


def get_roofs_by_batiment(conn, batiment_id):
    """
    Fetch all roofs for a building.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
    
    Returns:
        List of dictionaries containing roof data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT t.*, tt.nom_type, tt.k_toiture FROM toiture t
        JOIN type_toiture tt ON t.id_type_toiture = tt.id
        WHERE t.id_batiment = %s ORDER BY t.numero_toiture
    """, (batiment_id,))
    return cur.fetchall()


def get_next_roof_number(conn, batiment_id):
    """
    Get the next roof number for a building.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
    
    Returns:
        Next roof number (integer).
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT COUNT(*) as cnt FROM toiture WHERE id_batiment = %s",
        (batiment_id,)
    )
    return cur.fetchone()['cnt'] + 1


def insert_roof(conn, batiment_id, numero, condition, surface, type_id, deperdition):
    """
    Insert a new roof record.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
        numero: Roof number.
        condition: Condition of the roof.
        surface: Surface area in m².
        type_id: ID of the roof type.
        deperdition: Heat loss value in W/K.
    """
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO toiture (id_batiment, numero_toiture, etat_toiture,
                            surface_toit, id_type_toiture, deperdition_toiture)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (batiment_id, numero, condition, surface, type_id, deperdition))


def get_roof_type_k(conn, type_id):
    """
    Get the thermal transmission coefficient for a roof type.
    
    Args:
        conn: Active database connection.
        type_id: ID of the roof type.
    
    Returns:
        Thermal transmission coefficient as float.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT k_toiture FROM type_toiture WHERE id = %s", (type_id,))
    result = cur.fetchone()
    return float(result['k_toiture']) if result else 0.0


def get_all_roof_types(conn):
    """
    Fetch all roof types.
    
    Args:
        conn: Active database connection.
    
    Returns:
        List of dictionaries with roof type data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM type_toiture")
    return cur.fetchall()
