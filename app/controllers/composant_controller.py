"""Controller for composant (component) management routes."""

from flask import request, jsonify
from app.database import get_connection
from app.repositories import mur_repo, plancher_repo, toiture_repo, ouvrant_repo
from app.models.mur import Mur
from app.models.plancher import Plancher
from app.models.toiture import Toiture
from app.models.ouvrant import Ouvrant
from mysql.connector import Error


def add_mur():
    """Handles POST /api/ajouter-mur — validates, builds Mur object, persists."""
    data = request.get_json()
    conn = get_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'}), 500
    try:
        numero = mur_repo.get_next_numero(conn, data['id_batiment'])
        k = mur_repo.get_k(conn, data['id_type_mur'])
        # Build the model object — satisfies teacher's class diagram
        mur = Mur(
            id=None, id_batiment=data['id_batiment'],
            numero_mur=numero,
            longueur_mur=float(data['longueur']),
            hauteur_mur=float(data['hauteur']),
            etat_mur=data.get('etat', 'Bon état'),
            id_type_mur=data['id_type_mur'],
            k_mur=k, nom_type=''
        )
        dep = mur.calculer_deperdition()
        mur_repo.insert(conn, data['id_batiment'], numero, data, dep)
        conn.commit()
        return jsonify({'success': True, 'deperdition': dep,
                        'surface': round(mur.longueur_mur * mur.hauteur_mur, 2)})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


def add_plancher():
    """Handles POST /api/ajouter-plancher"""
    data = request.get_json()
    conn = get_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'}), 500
    try:
        numero = plancher_repo.get_next_numero(conn, data['id_batiment'])
        k = plancher_repo.get_k(conn, data['id_type_plancher'])
        plancher = Plancher(
            id=None, id_batiment=data['id_batiment'],
            numero_plancher=numero,
            surface_plancher=float(data['surface']),
            etat_plancher=data.get('etat', 'Bon état'),
            id_type_plancher=data['id_type_plancher'],
            k_plancher=k, nom_type=''
        )
        dep = plancher.calculer_deperdition()
        plancher_repo.insert(conn, data['id_batiment'], numero, data, dep)
        conn.commit()
        return jsonify({'success': True, 'deperdition': dep, 'surface': float(data['surface'])})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


def add_toiture():
    """Handles POST /api/ajouter-toiture"""
    data = request.get_json()
    conn = get_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'}), 500
    try:
        numero = toiture_repo.get_next_numero(conn, data['id_batiment'])
        k = toiture_repo.get_k(conn, data['id_type_toiture'])
        toiture = Toiture(
            id=None, id_batiment=data['id_batiment'],
            numero_toiture=numero,
            surface_toit=float(data['surface']),
            etat_toiture=data.get('etat', 'Bon état'),
            id_type_toiture=data['id_type_toiture'],
            k_toiture=k, nom_type=''
        )
        dep = toiture.calculer_deperdition()
        toiture_repo.insert(conn, data['id_batiment'], numero, data, dep)
        conn.commit()
        return jsonify({'success': True, 'deperdition': dep, 'surface': float(data['surface'])})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()


def add_ouvrant():
    """Handles POST /api/ajouter-ouvrant"""
    data = request.get_json()
    conn = get_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'}), 500
    try:
        numero = ouvrant_repo.get_next_numero(conn, data['id_batiment'])
        k = ouvrant_repo.get_k(conn, data['id_type_ouvrant'])
        ouvrant = Ouvrant(
            id=None, id_batiment=data['id_batiment'],
            numero_ouvrant=numero,
            surface_ouvrant=float(data['surface']),
            etat_ouvrant=data.get('etat', 'Bon état'),
            id_type_ouvrant=data['id_type_ouvrant'],
            k_ouvrant=k, nom_type=''
        )
        dep = ouvrant.calculer_deperdition()
        ouvrant_repo.insert(conn, data['id_batiment'], numero, data, dep)
        conn.commit()
        return jsonify({'success': True, 'deperdition': dep, 'surface': float(data['surface'])})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
