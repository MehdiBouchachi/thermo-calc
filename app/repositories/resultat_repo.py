"""Repository for Resultat (calculation result) database operations."""


def find_by_batiment(conn, batiment_id: int) -> dict | None:
    """Returns the calculation result for a batiment, or None."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM resultat_calcul WHERE id_batiment = %s", (batiment_id,))
    return cur.fetchone()


def upsert(conn, batiment_id: int, dep_totale: float,
           consommation: float, classe: str) -> None:
    """Inserts or updates the result row for a batiment."""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        INSERT INTO resultat_calcul
            (id_batiment, deperdition_totale, consommation_kwh, classe_energetique)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            deperdition_totale  = VALUES(deperdition_totale),
            consommation_kwh    = VALUES(consommation_kwh),
            classe_energetique  = VALUES(classe_energetique),
            date_calcul         = CURRENT_TIMESTAMP
    """, (batiment_id, round(dep_totale, 3), round(consommation, 3), classe))
