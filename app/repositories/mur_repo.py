# thermocalc/app/repositories/mur_repo.py
"""
Repository for Mur (Wall) database operations.
Handles SQL queries for wall component management.
"""


def get_walls_by_batiment(conn, batiment_id):
    """
    Fetch all walls for a building.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
    
    Returns:
        List of dictionaries containing wall data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT m.*, tm.nom_type, tm.k_mur FROM mur m
        JOIN type_mur tm ON m.id_type_mur = tm.id
        WHERE m.id_batiment = %s ORDER BY m.numero_mur
    """, (batiment_id,))
    return cur.fetchall()


def get_next_wall_number(conn, batiment_id):
    """
    Get the next wall number for a building.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
    
    Returns:
        Next wall number (integer).
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT COUNT(*) as cnt FROM mur WHERE id_batiment = %s",
        (batiment_id,)
    )
    return cur.fetchone()['cnt'] + 1


def insert_wall(conn, batiment_id, numero, length, height, condition, type_id, deperdition):
    """
    Insert a new wall record.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
        numero: Wall number.
        length: Length in meters.
        height: Height in meters.
        condition: Condition of the wall (e.g., 'Bon état').
        type_id: ID of the wall type.
        deperdition: Heat loss value in W/K.
    """
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO mur (id_batiment, numero_mur, longueur_mur, hauteur_mur, etat_mur,
                        id_type_mur, deperdition_mur)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (batiment_id, numero, length, height, condition, type_id, deperdition))


def get_wall_type_k(conn, type_id):
    """
    Get the thermal transmission coefficient (k) for a wall type.
    
    Args:
        conn: Active database connection.
        type_id: ID of the wall type.
    
    Returns:
        Thermal transmission coefficient as float.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT k_mur FROM type_mur WHERE id = %s", (type_id,))
    result = cur.fetchone()
    return float(result['k_mur']) if result else 0.0


def get_all_wall_types(conn):
    """
    Fetch all wall types.
    
    Args:
        conn: Active database connection.
    
    Returns:
        List of dictionaries with wall type data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM type_mur")
    return cur.fetchall()
