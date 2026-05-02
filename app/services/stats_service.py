"""Statistics service for overview and distribution data."""


def get_overview(conn) -> dict:
    """Returns global stats: total buildings, calculated count, average consumption, class distribution."""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) as total FROM batiment")
    total = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM resultat_calcul")
    calcules = cur.fetchone()['total']
    cur.execute("""
        SELECT classe_energetique, COUNT(*) as nb
        FROM resultat_calcul GROUP BY classe_energetique ORDER BY classe_energetique
    """)
    classes_data = cur.fetchall()
    cur.execute("SELECT AVG(consommation_kwh) as moy FROM resultat_calcul")
    row = cur.fetchone()
    moyenne = round(row['moy'], 1) if row['moy'] else 0
    return {
        'stats': {'total': total, 'calcules': calcules, 'moyenne': moyenne},
        'classes_data': classes_data
    }
