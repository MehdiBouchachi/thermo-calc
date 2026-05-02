# thermocalc/app/repositories/resultat_repo.py
"""
Repository for Resultat Calcul (Calculation Results) database operations.
Handles SQL queries for thermal calculation results.
"""


def get_result_by_batiment(conn, batiment_id):
    """
    Fetch calculation result for a building.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
    
    Returns:
        Dictionary with result data, or None if not found.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM resultat_calcul WHERE id_batiment = %s",
        (batiment_id,)
    )
    return cur.fetchone()


def insert_or_update_result(conn, batiment_id, deperdition_totale, consommation_kwh, classe):
    """
    Insert or update calculation results for a building.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
        deperdition_totale: Total heat loss in W/K.
        consommation_kwh: Annual energy consumption in kWh/m²/an.
        classe: Energy class (A-G).
    """
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO resultat_calcul
        (id_batiment, deperdition_totale, consommation_kwh, classe_energetique)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            deperdition_totale = VALUES(deperdition_totale),
            consommation_kwh = VALUES(consommation_kwh),
            classe_energetique = VALUES(classe_energetique),
            date_calcul = CURRENT_TIMESTAMP
    """, (batiment_id, deperdition_totale, consommation_kwh, classe))


def sum_deperditions(conn, batiment_id, table_name):
    """
    Sum heat loss from a specific component table.
    
    Args:
        conn: Active database connection.
        batiment_id: ID of the building.
        table_name: Name of the component table (mur, plancher, toiture, ouvrant).
    
    Returns:
        Total heat loss value as float.
    """
    column_map = {
        'mur': 'deperdition_mur',
        'plancher': 'deperdition_plancher',
        'toiture': 'deperdition_toiture',
        'ouvrant': 'deperdition_ouvrant',
    }
    
    column = column_map.get(table_name, 'deperdition_mur')
    query = f"SELECT COALESCE(SUM({column}), 0) as total FROM {table_name} WHERE id_batiment = %s"
    
    cur = conn.cursor(dictionary=True)
    cur.execute(query, (batiment_id,))
    result = cur.fetchone()
    return float(result['total']) if result else 0.0


def get_all_results(conn):
    """
    Fetch all calculation results.
    
    Args:
        conn: Active database connection.
    
    Returns:
        List of dictionaries with result data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM resultat_calcul")
    return cur.fetchall()


def count_buildings_by_class(conn):
    """
    Count buildings grouped by energy class.
    
    Args:
        conn: Active database connection.
    
    Returns:
        List of dictionaries with classe_energetique and count.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT classe_energetique, COUNT(*) as nb
        FROM resultat_calcul
        GROUP BY classe_energetique
        ORDER BY classe_energetique
    """)
    return cur.fetchall()


def get_average_consumption(conn):
    """
    Calculate average energy consumption across all buildings.
    
    Args:
        conn: Active database connection.
    
    Returns:
        Average consumption as float, or 0 if no data.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT AVG(consommation_kwh) as moy FROM resultat_calcul")
    row = cur.fetchone()
    return float(row['moy']) if row and row['moy'] else 0.0


def count_total_buildings(conn):
    """
    Count total number of buildings.
    
    Args:
        conn: Active database connection.
    
    Returns:
        Total count as integer.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) as total FROM batiment")
    return cur.fetchone()['total']


def count_calculated_buildings(conn):
    """
    Count buildings with completed calculations.
    
    Args:
        conn: Active database connection.
    
    Returns:
        Count of calculated buildings as integer.
    """
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) as total FROM resultat_calcul")
    return cur.fetchone()['total']
