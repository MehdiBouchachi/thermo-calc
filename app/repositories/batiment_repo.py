"""Repository for Batiment (building) database operations."""


def find_all(conn) -> list[dict]:
    """Returns all batiments joined with zone and result data, newest first."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT b.*, z.nom_zone, r.classe_energetique, r.consommation_kwh
        FROM batiment b
        LEFT JOIN zone_climatique z ON b.id_zone_climatique = z.id
        LEFT JOIN resultat_calcul r ON b.id = r.id_batiment
        ORDER BY b.date_creation DESC
    """)
    return cur.fetchall()


def find_by_id(conn, batiment_id: int) -> dict | None:
    """Returns a single batiment row with zone info, or None."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT b.*, z.nom_zone FROM batiment b
        LEFT JOIN zone_climatique z ON b.id_zone_climatique = z.id
        WHERE b.id = %s
    """, (batiment_id,))
    return cur.fetchone()


def insert(conn, data: dict) -> int:
    """Inserts a new batiment row. Returns the new row id."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        INSERT INTO batiment (code_batiment, adresse_batiment, coordonnees_geo,
            type_batiment, surface, volume, annee_construction,
            nombre_niveaux, nombre_occupants, id_zone_climatique)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get('code_batiment'), data.get('adresse_batiment'),
        data.get('coordonnees_geo', ''), data.get('type_batiment'),
        float(data.get('surface', 0)),
        float(data.get('volume')) if data.get('volume') else None,
        int(data.get('annee_construction')) if data.get('annee_construction') else None,
        int(data.get('nombre_niveaux', 1)),
        int(data.get('nombre_occupants', 0)),
        int(data.get('id_zone_climatique')) if data.get('id_zone_climatique') else None
    ))
    return cur.lastrowid


def delete(conn, batiment_id: int) -> None:
    """Deletes a batiment by id. Cascades to all composants via FK."""
    cur = conn.cursor(dictionary=True)
    cur.execute("DELETE FROM batiment WHERE id = %s", (batiment_id,))


def find_all_zones(conn) -> list[dict]:
    """Returns all climate zones ordered by name."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM zone_climatique ORDER BY nom_zone")
    return cur.fetchall()


def find_all_sources(conn) -> list[dict]:
    """Returns all energy sources ordered by name."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM source_energie ORDER BY nom_source")
    return cur.fetchall()


def insert_sources(conn, batiment_id: int, source_ids: list) -> None:
    """Links a list of energy source ids to a batiment."""
    cur = conn.cursor(dictionary=True)
    for sid in source_ids:
        cur.execute(
            "INSERT INTO batiment_source VALUES (%s, %s)",
            (batiment_id, sid)
        )
