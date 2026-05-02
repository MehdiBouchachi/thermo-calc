"""Controller for calculation routes."""

from flask import jsonify, render_template
from app.database import get_connection
from app.repositories import batiment_repo
from app.services import calcul_service, stats_service
from mysql.connector import Error


def run_calcul(batiment_id: int):
    """Handles POST /api/calculer/<batiment_id> — runs the full deperdition calculation."""
    conn = get_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'}), 500
    try:
        row = batiment_repo.find_by_id(conn, batiment_id)
        if not row:
            return jsonify({'success': False, 'message': 'Bâtiment introuvable'}), 404
        result = calcul_service.compute(conn, batiment_id, float(row['surface']))
        conn.commit()
        return jsonify({'success': True, **result})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


def get_stats():
    """Handles GET /statistiques — returns stats page."""
    conn = get_connection()
    data = stats_service.get_overview(conn) if conn else {'stats': {}, 'classes_data': []}
    if conn:
        conn.close()
    return render_template('statistiques/index.html', **data)
