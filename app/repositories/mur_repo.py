"""Repository for Mur (wall) database operations."""


def find_all_types(conn) -> list[dict]:
    """Returns all wall types."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM type_mur")
    return cur.fetchall()


def find_by_batiment(conn, batiment_id: int) -> list[dict]:
    """Returns all mur rows for a batiment, joined with type data."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT m.*, tm.nom_type, tm.k_mur FROM mur m
        JOIN type_mur tm ON m.id_type_mur = tm.id
        WHERE m.id_batiment = %s ORDER BY m.numero_mur
    """, (batiment_id,))
    return cur.fetchall()


def get_next_numero(conn, batiment_id: int) -> int:
    """Returns the next wall number for a batiment."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) as cnt FROM mur WHERE id_batiment = %s", (batiment_id,))
    return cur.fetchone()['cnt'] + 1


def get_k(conn, type_id: int) -> float:
    """Returns the k_mur coefficient for a given type id."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT k_mur FROM type_mur WHERE id = %s", (type_id,))
    return float(cur.fetchone()['k_mur'])


def insert(conn, batiment_id: int, numero: int, data: dict, deperdition: float) -> None:
    """Inserts a new mur row with pre-computed deperdition."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        INSERT INTO mur (id_batiment, numero_mur, longueur_mur, hauteur_mur,
                         etat_mur, id_type_mur, deperdition_mur)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (batiment_id, numero, data['longueur'], data['hauteur'],
          data.get('etat', 'Bon état'), data['id_type_mur'], deperdition))
