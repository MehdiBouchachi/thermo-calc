# thermocalc/app/routes/api.py
"""
API routes for component management and calculations.
Handles AJAX requests for adding components and performing calculations.
"""

from flask import Blueprint, request, jsonify
from mysql.connector import Error
from app.database import get_db_connection
from app.services import calcul_service

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/ajouter-mur', methods=['POST'])
def ajouter_mur():
    """
    Add a wall component to a building.
    
    JSON body:
        - id_batiment: Building ID
        - id_type_mur: Wall type ID
        - longueur: Wall length in meters
        - hauteur: Wall height in meters
        - etat: Condition (default: 'Bon état')
    
    Returns:
        JSON response with success status and deperdition value.
    """
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'})
    
    try:
        result = calcul_service.add_wall_component(
            conn,
            data['id_batiment'],
            data['id_type_mur'],
            data['longueur'],
            data['hauteur'],
            data.get('etat', 'Bon état')
        )
        conn.commit()
        return jsonify({'success': True, **result})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@bp.route('/ajouter-plancher', methods=['POST'])
def ajouter_plancher():
    """
    Add a floor component to a building.
    
    JSON body:
        - id_batiment: Building ID
        - id_type_plancher: Floor type ID
        - surface: Surface area in m²
        - etat: Condition (default: 'Bon état')
    
    Returns:
        JSON response with success status and deperdition value.
    """
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'})
    
    try:
        result = calcul_service.add_floor_component(
            conn,
            data['id_batiment'],
            data['id_type_plancher'],
            data['surface'],
            data.get('etat', 'Bon état')
        )
        conn.commit()
        return jsonify({'success': True, **result})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@bp.route('/ajouter-toiture', methods=['POST'])
def ajouter_toiture():
    """
    Add a roof component to a building.
    
    JSON body:
        - id_batiment: Building ID
        - id_type_toiture: Roof type ID
        - surface: Surface area in m²
        - etat: Condition (default: 'Bon état')
    
    Returns:
        JSON response with success status and deperdition value.
    """
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'})
    
    try:
        result = calcul_service.add_roof_component(
            conn,
            data['id_batiment'],
            data['id_type_toiture'],
            data['surface'],
            data.get('etat', 'Bon état')
        )
        conn.commit()
        return jsonify({'success': True, **result})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@bp.route('/ajouter-ouvrant', methods=['POST'])
def ajouter_ouvrant():
    """
    Add a window/opening component to a building.
    
    JSON body:
        - id_batiment: Building ID
        - id_type_ouvrant: Opening type ID
        - surface: Surface area in m²
        - etat: Condition (default: 'Bon état')
    
    Returns:
        JSON response with success status and deperdition value.
    """
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'})
    
    try:
        result = calcul_service.add_opening_component(
            conn,
            data['id_batiment'],
            data['id_type_ouvrant'],
            data['surface'],
            data.get('etat', 'Bon état')
        )
        conn.commit()
        return jsonify({'success': True, **result})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@bp.route('/calculer/<int:batiment_id>', methods=['POST'])
def calculer_deperdition(batiment_id):
    """
    Compute thermal calculation for a building.
    
    Args:
        batiment_id: ID of the building.
    
    Returns:
        JSON response with complete calculation results.
    """
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'})
    
    try:
        result = calcul_service.compute_deperdition(conn, batiment_id)
        conn.commit()
        return jsonify({'success': True, **result})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()
