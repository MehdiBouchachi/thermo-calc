# thermocalc/app/routes/batiments.py
"""
Building management routes.
Handles requests for viewing, creating, and deleting buildings.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import get_db_connection
from app.services import batiment_service

bp = Blueprint('batiments', __name__, url_prefix='')


@bp.route('/')
def index():
    """
    Display list of all buildings.
    
    Returns:
        Rendered index template with building list.
    """
    conn = get_db_connection()
    batiments = []
    if conn:
        batiments = batiment_service.get_all_buildings(conn)
        conn.close()
    return render_template('batiments/index.html', batiments=batiments)


@bp.route('/batiment/nouveau', methods=['GET', 'POST'])
def nouveau_batiment():
    """
    Handle building creation form display and submission.
    
    GET: Display empty form with zones and energy sources.
    POST: Validate and create new building record.
    
    Returns:
        On GET: Rendered form template.
        On POST: Redirect to building detail page.
    """
    conn = get_db_connection()
    form_options = {}
    
    if conn:
        form_options = batiment_service.get_form_options(conn)
    
    if request.method == 'POST':
        if conn:
            try:
                batiment_id = batiment_service.create_building(conn, request.form)
                conn.commit()
                flash('Bâtiment créé avec succès !', 'success')
                return redirect(url_for('batiments.detail_batiment', batiment_id=batiment_id))
            except Exception as e:
                conn.rollback()
                flash(f'Erreur lors de la création: {str(e)}', 'danger')
            finally:
                conn.close()
        return render_template('batiments/nouveau.html', 
                             zones=form_options.get('zones', []),
                             sources=form_options.get('sources', []))
    
    return render_template('batiments/nouveau.html',
                         zones=form_options.get('zones', []),
                         sources=form_options.get('sources', []))


@bp.route('/batiment/<int:batiment_id>')
def detail_batiment(batiment_id):
    """
    Display detailed information for a building.
    
    Args:
        batiment_id: ID of the building.
    
    Returns:
        Rendered detail template with building and component data.
    """
    conn = get_db_connection()
    if not conn:
        flash('Erreur de connexion à la base de données', 'danger')
        return redirect(url_for('batiments.index'))
    
    try:
        details = batiment_service.get_building_details(conn, batiment_id)
        if not details:
            flash('Bâtiment introuvable', 'danger')
            return redirect(url_for('batiments.index'))
        
        return render_template('batiments/detail.html', **details)
    finally:
        conn.close()


@bp.route('/batiment/<int:batiment_id>/supprimer', methods=['POST'])
def supprimer_batiment(batiment_id):
    """
    Delete a building.
    
    Args:
        batiment_id: ID of the building to delete.
    
    Returns:
        Redirect to building list.
    """
    conn = get_db_connection()
    if conn:
        try:
            batiment_service.delete_building(conn, batiment_id)
            conn.commit()
            flash('Bâtiment supprimé.', 'info')
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de la suppression: {str(e)}', 'danger')
        finally:
            conn.close()
    return redirect(url_for('batiments.index'))
