"""Controller for building management routes."""

from flask import render_template, request, redirect, url_for, flash
from app.database import get_connection
from app.services import batiment_service
from mysql.connector import Error


def list_batiments():
    """Handles GET / — renders the building list page."""
    conn = get_connection()
    batiments = batiment_service.get_all(conn) if conn else []
    if conn:
        conn.close()
    return render_template('batiments/index.html', batiments=batiments)


def create_batiment():
    """Handles GET+POST /batiment/nouveau"""
    conn = get_connection()
    form_data = batiment_service.get_form_data(conn) if conn else {'zones': [], 'sources': []}
    if conn:
        conn.close()

    if request.method == 'POST':
        conn = get_connection()
        if conn:
            try:
                batiment_id = batiment_service.create(
                    conn,
                    request.form.to_dict(),
                    request.form.getlist('sources')
                )
                conn.commit()
                flash('Bâtiment créé avec succès !', 'success')
                return redirect(url_for('batiments.detail_batiment', batiment_id=batiment_id))
            except Error as e:
                conn.rollback()
                flash(f'Erreur lors de la création: {e}', 'danger')
            finally:
                conn.close()

    return render_template('batiments/nouveau.html', **form_data)


def detail_batiment(batiment_id: int):
    """Handles GET /batiment/<id> — renders full detail page."""
    conn = get_connection()
    if not conn:
        flash('Erreur de connexion à la base de données', 'danger')
        return redirect(url_for('batiments.list_batiments'))
    detail = batiment_service.get_detail(conn, batiment_id)
    conn.close()
    if not detail:
        flash('Bâtiment introuvable', 'danger')
        return redirect(url_for('batiments.list_batiments'))
    return render_template('batiments/detail.html', **detail)


def delete_batiment(batiment_id: int):
    """Handles POST /batiment/<id>/supprimer"""
    conn = get_connection()
    if conn:
        batiment_service.delete(conn, batiment_id)
        conn.commit()
        conn.close()
        flash('Bâtiment supprimé.', 'info')
    return redirect(url_for('batiments.list_batiments'))
