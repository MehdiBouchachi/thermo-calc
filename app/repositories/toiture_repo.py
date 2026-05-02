"""Repository for Toiture (roof) database operations."""


def find_all_types(conn) -> list[dict]:
    """Returns all roof types."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM type_toiture")
    return cur.fetchall()


def find_by_batiment(conn, batiment_id: int) -> list[dict]:
    """Returns all toiture rows for a batiment, joined with type data."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT t.*, tt.nom_type, tt.k_toiture FROM toiture t
        JOIN type_toiture tt ON t.id_type_toiture = tt.id
        WHERE t.id_batiment = %s ORDER BY t.numero_toiture
    """, (batiment_id,))
    return cur.fetchall()


def get_next_numero(conn, batiment_id: int) -> int:
    """Returns the next roof number for a batiment."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) as cnt FROM toiture WHERE id_batiment = %s", (batiment_id,))
    return cur.fetchone()['cnt'] + 1


def get_k(conn, type_id: int) -> float:
    """Returns the k_toiture coefficient for a given type id."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT k_toiture FROM type_toiture WHERE id = %s", (type_id,))
    return float(cur.fetchone()['k_toiture'])


def insert(conn, batiment_id: int, numero: int, data: dict, deperdition: float) -> None:
    """Inserts a new toiture row with pre-computed deperdition."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        INSERT INTO toiture (id_batiment, numero_toiture, surface_toit,
                             etat_toiture, id_type_toiture, deperdition_toiture)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (batiment_id, numero, data['surface'], data.get('etat', 'Bon état'),
          data['id_type_toiture'], deperdition))
