"""Repository for Ouvrant (opening) database operations."""


def find_all_types(conn) -> list[dict]:
    """Returns all opening types."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM type_ouvrant")
    return cur.fetchall()


def find_by_batiment(conn, batiment_id: int) -> list[dict]:
    """Returns all ouvrant rows for a batiment, joined with type data."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT o.*, to_type.nom_type, to_type.k_ouvrant FROM ouvrant o
        JOIN type_ouvrant to_type ON o.id_type_ouvrant = to_type.id
        WHERE o.id_batiment = %s ORDER BY o.numero_ouvrant
    """, (batiment_id,))
    return cur.fetchall()


def get_next_numero(conn, batiment_id: int) -> int:
    """Returns the next opening number for a batiment."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) as cnt FROM ouvrant WHERE id_batiment = %s", (batiment_id,))
    return cur.fetchone()['cnt'] + 1


def get_k(conn, type_id: int) -> float:
    """Returns the k_ouvrant coefficient for a given type id."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT k_ouvrant FROM type_ouvrant WHERE id = %s", (type_id,))
    return float(cur.fetchone()['k_ouvrant'])


def insert(conn, batiment_id: int, numero: int, data: dict, deperdition: float) -> None:
    """Inserts a new ouvrant row with pre-computed deperdition."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        INSERT INTO ouvrant (id_batiment, numero_ouvrant, surface_ouvrant,
                             etat_ouvrant, id_type_ouvrant, deperdition_ouvrant)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (batiment_id, numero, data['surface'], data.get('etat', 'Bon état'),
          data['id_type_ouvrant'], deperdition))
