"""Repository for Plancher (floor) database operations."""


def find_all_types(conn) -> list[dict]:
    """Returns all floor types."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM type_plancher")
    return cur.fetchall()


def find_by_batiment(conn, batiment_id: int) -> list[dict]:
    """Returns all plancher rows for a batiment, joined with type data."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT p.*, tp.nom_type, tp.k_plancher FROM plancher p
        JOIN type_plancher tp ON p.id_type_plancher = tp.id
        WHERE p.id_batiment = %s ORDER BY p.numero_plancher
    """, (batiment_id,))
    return cur.fetchall()


def get_next_numero(conn, batiment_id: int) -> int:
    """Returns the next floor number for a batiment."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) as cnt FROM plancher WHERE id_batiment = %s", (batiment_id,))
    return cur.fetchone()['cnt'] + 1


def get_k(conn, type_id: int) -> float:
    """Returns the k_plancher coefficient for a given type id."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT k_plancher FROM type_plancher WHERE id = %s", (type_id,))
    return float(cur.fetchone()['k_plancher'])


def insert(conn, batiment_id: int, numero: int, data: dict, deperdition: float) -> None:
    """Inserts a new plancher row with pre-computed deperdition."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        INSERT INTO plancher (id_batiment, numero_plancher, surface_plancher,
                              etat_plancher, id_type_plancher, deperdition_plancher)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (batiment_id, numero, data['surface'], data.get('etat', 'Bon état'),
          data['id_type_plancher'], deperdition))
