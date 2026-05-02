# thermocalc/app/routes/stats.py
"""
Statistics and reporting routes.
Displays energy class distribution and overall statistics.
"""

from flask import Blueprint, render_template
from app.database import get_db_connection
from app.repositories import resultat_repo

bp = Blueprint('stats', __name__, url_prefix='')


@bp.route('/statistiques')
def statistiques():
    """
    Display statistics dashboard with energy class distribution.
    
    Returns:
        Rendered statistics template with aggregated data.
    """
    conn = get_db_connection()
    stats = {}
    classes_data = []
    
    if conn:
        try:
            stats['total'] = resultat_repo.count_total_buildings(conn)
            stats['calcules'] = resultat_repo.count_calculated_buildings(conn)
            classes_data = resultat_repo.count_buildings_by_class(conn)
            stats['moyenne'] = round(resultat_repo.get_average_consumption(conn), 1)
        finally:
            conn.close()
    
    return render_template('statistiques/index.html', stats=stats, classes_data=classes_data)
