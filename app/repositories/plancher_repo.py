# thermocalc/app/repositories/plancher_repo.py
"""
Repository for Plancher (Floor) database operations.
Handles SQL queries for floor component management.
"""


def get_floors_by_batiment(conn, batiment_id):
    """
    Fetch all floors for a building.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
    
    Returns:
        List of dictionaries containing floor data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT p.*, tp.nom_type, tp.k_plancher FROM plancher p
        JOIN type_plancher tp ON p.id_type_plancher = tp.id
        WHERE p.id_batiment = %s ORDER BY p.numero_plancher
    """, (batiment_id,))
    return cur.fetchall()


def get_next_floor_number(conn, batiment_id):
    """
    Get the next floor number for a building.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
    
    Returns:
        Next floor number (integer).
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT COUNT(*) as cnt FROM plancher WHERE id_batiment = %s",
        (batiment_id,)
    )
    return cur.fetchone()['cnt'] + 1


def insert_floor(conn, batiment_id, numero, condition, surface, type_id, deperdition):
    """
    Insert a new floor record.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
        numero: Floor number.
        condition: Condition of the floor.
        surface: Surface area in m².
        type_id: ID of the floor type.
        deperdition: Heat loss value in W/K.
    """
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO plancher (id_batiment, numero_plancher, etat_plancher,
                             surface_plancher, id_type_plancher, deperdition_plancher)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (batiment_id, numero, condition, surface, type_id, deperdition))


def get_floor_type_k(conn, type_id):
    """
    Get the thermal transmission coefficient for a floor type.
    
    Args:
        conn: Active database connection.
        type_id: ID of the floor type.
    
    Returns:
        Thermal transmission coefficient as float.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT k_plancher FROM type_plancher WHERE id = %s", (type_id,))
    result = cur.fetchone()
    return float(result['k_plancher']) if result else 0.0


def get_all_floor_types(conn):
    """
    Fetch all floor types.
    
    Args:
        conn: Active database connection.
    
    Returns:
        List of dictionaries with floor type data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM type_plancher")
    return cur.fetchall()
