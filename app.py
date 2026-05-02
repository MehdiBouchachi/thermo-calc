"""
Application Web - Calcul de Déperditions Thermiques d'un Bâtiment
Département d'informatique - TP 2026 SIA M1-IL
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'thermique_secret_key_2026'

# ============================================================
# CONFIGURATION BASE DE DONNÉES
# ============================================================
DB_CONFIG = {
    'host': 'localhost',        # Hôte MySQL
    'user': 'root',             # Utilisateur MySQL
    'password': 'Malak2003',             # Mot de passe MySQL
    'database': 'thermique_db',
    'charset': 'utf8mb4'
}


def get_db_connection():
    """Retourne une connexion à la base de données."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None


def get_cursor(conn):
    return conn.cursor(dictionary=True)


# ============================================================
# ROUTES PRINCIPALES
# ============================================================

@app.route('/')
def index():
    """Page d'accueil - liste des bâtiments."""
    conn = get_db_connection()
    batiments = []
    if conn:
        cur = get_cursor(conn)
        cur.execute("""
            SELECT b.*, z.nom_zone, r.classe_energetique, r.consommation_kwh
            FROM batiment b
            LEFT JOIN zone_climatique z ON b.id_zone_climatique = z.id
            LEFT JOIN resultat_calcul r ON b.id = r.id_batiment
            ORDER BY b.date_creation DESC
        """)
        batiments = cur.fetchall()
        app.logger.debug('Fetched %s batiments from DB', len(batiments))
        conn.close()
    return render_template('index.html', batiments=batiments)


@app.route('/batiment/nouveau', methods=['GET', 'POST'])
def nouveau_batiment():
    """Formulaire de création d'un nouveau bâtiment."""
    conn = get_db_connection()
    zones = []
    sources = []
    if conn:
        cur = get_cursor(conn)
        cur.execute("SELECT * FROM zone_climatique ORDER BY nom_zone")
        zones = cur.fetchall()
        cur.execute("SELECT * FROM source_energie ORDER BY nom_source")
        sources = cur.fetchall()
        conn.close()

    if request.method == 'POST':
        data = request.form
        app.logger.debug('Form POST data: %s', data.to_dict(flat=False))
        conn = get_db_connection()
        if conn:
            try:
                cur = get_cursor(conn)
                # Insérer le bâtiment
                cur.execute("""
                    INSERT INTO batiment (code_batiment, adresse_batiment, coordonnees_geo,
                        type_batiment, surface, volume, annee_construction,
                        nombre_niveaux, nombre_occupants, id_zone_climatique)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    data.get('code_batiment'),
                    data.get('adresse_batiment'),
                    data.get('coordonnees_geo', ''),
                    data.get('type_batiment'),
                    float(data.get('surface', 0)),
                    float(data.get('volume', 0)) if data.get('volume') else None,
                    int(data.get('annee_construction')) if data.get('annee_construction') else None,
                    int(data.get('nombre_niveaux', 1)),
                    int(data.get('nombre_occupants', 0)),
                    int(data.get('id_zone_climatique')) if data.get('id_zone_climatique') else None
                ))
                batiment_id = cur.lastrowid
                app.logger.debug('Inserted batiment, lastrowid=%s, rowcount=%s', batiment_id, getattr(cur, 'rowcount', None))

                # Sources d'énergie
                sources_sel = request.form.getlist('sources')
                app.logger.debug('Selected sources: %s', sources_sel)
                for sid in sources_sel:
                    cur.execute("INSERT INTO batiment_source VALUES (%s, %s)", (batiment_id, sid))
                conn.commit()
                app.logger.debug('Committed new batiment and batiment_source rows')
                flash('Bâtiment créé avec succès !', 'success')
                return redirect(url_for('detail_batiment', batiment_id=batiment_id))
            except Error as e:
                conn.rollback()
                app.logger.exception('Erreur lors de la création du bâtiment')
                flash(f'Erreur lors de la création: {e}', 'danger')
            finally:
                conn.close()

    return render_template('nouveau_batiment.html', zones=zones, sources=sources)


@app.route('/batiment/<int:batiment_id>')
def detail_batiment(batiment_id):
    """Détail d'un bâtiment avec ses composants."""
    conn = get_db_connection()
    if not conn:
        flash('Erreur de connexion à la base de données', 'danger')
        return redirect(url_for('index'))

    cur = get_cursor(conn)

    cur.execute("""
        SELECT b.*, z.nom_zone FROM batiment b
        LEFT JOIN zone_climatique z ON b.id_zone_climatique = z.id
        WHERE b.id = %s
    """, (batiment_id,))
    batiment = cur.fetchone()

    if not batiment:
        flash('Bâtiment introuvable', 'danger')
        return redirect(url_for('index'))

    cur.execute("""
        SELECT m.*, tm.nom_type, tm.k_mur FROM mur m
        JOIN type_mur tm ON m.id_type_mur = tm.id
        WHERE m.id_batiment = %s ORDER BY m.numero_mur
    """, (batiment_id,))
    murs = cur.fetchall()

    cur.execute("""
        SELECT p.*, tp.nom_type, tp.k_plancher FROM plancher p
        JOIN type_plancher tp ON p.id_type_plancher = tp.id
        WHERE p.id_batiment = %s ORDER BY p.numero_plancher
    """, (batiment_id,))
    planchers = cur.fetchall()

    cur.execute("""
        SELECT t.*, tt.nom_type, tt.k_toiture FROM toiture t
        JOIN type_toiture tt ON t.id_type_toiture = tt.id
        WHERE t.id_batiment = %s ORDER BY t.numero_toiture
    """, (batiment_id,))
    toitures = cur.fetchall()

    cur.execute("""
        SELECT o.*, to2.nom_type, to2.k_ouvrant FROM ouvrant o
        JOIN type_ouvrant to2 ON o.id_type_ouvrant = to2.id
        WHERE o.id_batiment = %s ORDER BY o.numero_ouvrant
    """, (batiment_id,))
    ouvrants = cur.fetchall()

    cur.execute("""
        SELECT r.* FROM resultat_calcul r WHERE r.id_batiment = %s
    """, (batiment_id,))
    resultat = cur.fetchone()

    # Types pour les formulaires d'ajout
    cur.execute("SELECT * FROM type_mur")
    types_mur = cur.fetchall()
    cur.execute("SELECT * FROM type_plancher")
    types_plancher = cur.fetchall()
    cur.execute("SELECT * FROM type_toiture")
    types_toiture = cur.fetchall()
    cur.execute("SELECT * FROM type_ouvrant")
    types_ouvrant = cur.fetchall()

    conn.close()
    return render_template('detail_batiment.html',
        batiment=batiment, murs=murs, planchers=planchers,
        toitures=toitures, ouvrants=ouvrants, resultat=resultat,
        types_mur=types_mur, types_plancher=types_plancher,
        types_toiture=types_toiture, types_ouvrant=types_ouvrant)


# ============================================================
# ROUTES AJAX - AJOUT DE COMPOSANTS
# ============================================================

@app.route('/api/ajouter-mur', methods=['POST'])
def ajouter_mur():
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'})
    try:
        cur = get_cursor(conn)
        # Calculer numéro
        cur.execute("SELECT COUNT(*) as cnt FROM mur WHERE id_batiment=%s", (data['id_batiment'],))
        num = cur.fetchone()['cnt'] + 1
        # Calcul déperdition
        cur.execute("SELECT k_mur FROM type_mur WHERE id=%s", (data['id_type_mur'],))
        k = cur.fetchone()['k_mur']
        surface = float(data['longueur']) * float(data['hauteur'])
        dep = float(k) * surface

        cur.execute("""
            INSERT INTO mur (id_batiment, numero_mur, longueur_mur, hauteur_mur, etat_mur, id_type_mur, deperdition_mur)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (data['id_batiment'], num, data['longueur'], data['hauteur'],
              data.get('etat', 'Bon état'), data['id_type_mur'], dep))
        conn.commit()
        return jsonify({'success': True, 'deperdition': round(dep, 3), 'surface': round(surface, 2)})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@app.route('/api/ajouter-plancher', methods=['POST'])
def ajouter_plancher():
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'})
    try:
        cur = get_cursor(conn)
        cur.execute("SELECT COUNT(*) as cnt FROM plancher WHERE id_batiment=%s", (data['id_batiment'],))
        num = cur.fetchone()['cnt'] + 1
        cur.execute("SELECT k_plancher FROM type_plancher WHERE id=%s", (data['id_type_plancher'],))
        k = cur.fetchone()['k_plancher']
        dep = float(k) * float(data['surface'])

        cur.execute("""
            INSERT INTO plancher (id_batiment, numero_plancher, etat_plancher, surface_plancher, id_type_plancher, deperdition_plancher)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['id_batiment'], num, data.get('etat', 'Bon état'), data['surface'], data['id_type_plancher'], dep))
        conn.commit()
        return jsonify({'success': True, 'deperdition': round(dep, 3)})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@app.route('/api/ajouter-toiture', methods=['POST'])
def ajouter_toiture():
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'})
    try:
        cur = get_cursor(conn)
        cur.execute("SELECT COUNT(*) as cnt FROM toiture WHERE id_batiment=%s", (data['id_batiment'],))
        num = cur.fetchone()['cnt'] + 1
        cur.execute("SELECT k_toiture FROM type_toiture WHERE id=%s", (data['id_type_toiture'],))
        k = cur.fetchone()['k_toiture']
        dep = float(k) * float(data['surface'])

        cur.execute("""
            INSERT INTO toiture (id_batiment, numero_toiture, etat_toiture, surface_toit, id_type_toiture, deperdition_toiture)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['id_batiment'], num, data.get('etat', 'Bon état'), data['surface'], data['id_type_toiture'], dep))
        conn.commit()
        return jsonify({'success': True, 'deperdition': round(dep, 3)})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


@app.route('/api/ajouter-ouvrant', methods=['POST'])
def ajouter_ouvrant():
    data = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'})
    try:
        cur = get_cursor(conn)
        cur.execute("SELECT COUNT(*) as cnt FROM ouvrant WHERE id_batiment=%s", (data['id_batiment'],))
        num = cur.fetchone()['cnt'] + 1
        cur.execute("SELECT k_ouvrant FROM type_ouvrant WHERE id=%s", (data['id_type_ouvrant'],))
        k = cur.fetchone()['k_ouvrant']
        dep = float(k) * float(data['surface'])

        cur.execute("""
            INSERT INTO ouvrant (id_batiment, numero_ouvrant, surface_ouvrant, etat_ouvrant, id_type_ouvrant, deperdition_ouvrant)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['id_batiment'], num, data['surface'], data.get('etat', 'Bon état'), data['id_type_ouvrant'], dep))
        conn.commit()
        return jsonify({'success': True, 'deperdition': round(dep, 3)})
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


# ============================================================
# CALCUL DE LA DÉPERDITION GLOBALE
# ============================================================

@app.route('/api/calculer/<int:batiment_id>', methods=['POST'])
def calculer_deperdition(batiment_id):
    """Calcule la déperdition totale et classe le bâtiment."""
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Erreur DB'})
    try:
        cur = get_cursor(conn)

        # Récupérer surface bâtiment
        cur.execute("SELECT surface FROM batiment WHERE id=%s", (batiment_id,))
        bat = cur.fetchone()
        if not bat:
            return jsonify({'success': False, 'message': 'Bâtiment introuvable'})
        surface = float(bat['surface'])

        # Somme des déperditions
        cur.execute("SELECT COALESCE(SUM(deperdition_mur), 0) as total FROM mur WHERE id_batiment=%s", (batiment_id,))
        dep_murs = float(cur.fetchone()['total'])

        cur.execute("SELECT COALESCE(SUM(deperdition_plancher), 0) as total FROM plancher WHERE id_batiment=%s", (batiment_id,))
        dep_planchers = float(cur.fetchone()['total'])

        cur.execute("SELECT COALESCE(SUM(deperdition_toiture), 0) as total FROM toiture WHERE id_batiment=%s", (batiment_id,))
        dep_toitures = float(cur.fetchone()['total'])

        cur.execute("SELECT COALESCE(SUM(deperdition_ouvrant), 0) as total FROM ouvrant WHERE id_batiment=%s", (batiment_id,))
        dep_ouvrants = float(cur.fetchone()['total'])

        dep_totale = dep_murs + dep_planchers + dep_toitures + dep_ouvrants

        # Conversion en kWh/m²/an
        # Formule simplifiée : (déperdition * 2400h * facteur) / surface
        # Facteur 2400h représente les heures de chauffage annuelles estimées
        if surface > 0:
            consommation = (dep_totale * 2400) / (surface * 1000)
        else:
            consommation = 0

        # Classification énergétique
        classe = classifier(consommation)

        # Sauvegarder
        cur.execute("""
            INSERT INTO resultat_calcul (id_batiment, deperdition_totale, consommation_kwh, classe_energetique)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                deperdition_totale = VALUES(deperdition_totale),
                consommation_kwh = VALUES(consommation_kwh),
                classe_energetique = VALUES(classe_energetique),
                date_calcul = CURRENT_TIMESTAMP
        """, (batiment_id, round(dep_totale, 3), round(consommation, 3), classe))
        conn.commit()

        return jsonify({
            'success': True,
            'dep_murs': round(dep_murs, 3),
            'dep_planchers': round(dep_planchers, 3),
            'dep_toitures': round(dep_toitures, 3),
            'dep_ouvrants': round(dep_ouvrants, 3),
            'dep_totale': round(dep_totale, 3),
            'consommation': round(consommation, 3),
            'classe': classe
        })
    except Error as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()


def classifier(consommation):
    """Classifie un bâtiment selon sa consommation en kWh/m²/an."""
    if consommation <= 70:
        return 'A'
    elif consommation <= 110:
        return 'B'
    elif consommation <= 180:
        return 'C'
    elif consommation <= 250:
        return 'D'
    elif consommation <= 330:
        return 'E'
    elif consommation <= 420:
        return 'F'
    else:
        return 'G'


@app.route('/batiment/<int:batiment_id>/supprimer', methods=['POST'])
def supprimer_batiment(batiment_id):
    conn = get_db_connection()
    if conn:
        cur = get_cursor(conn)
        cur.execute("DELETE FROM batiment WHERE id=%s", (batiment_id,))
        conn.commit()
        conn.close()
        flash('Bâtiment supprimé.', 'info')
    return redirect(url_for('index'))


@app.route('/statistiques')
def statistiques():
    """Page de statistiques globales."""
    conn = get_db_connection()
    stats = {}
    classes_data = []
    if conn:
        cur = get_cursor(conn)
        cur.execute("SELECT COUNT(*) as total FROM batiment")
        stats['total'] = cur.fetchone()['total']
        cur.execute("SELECT COUNT(*) as total FROM resultat_calcul")
        stats['calcules'] = cur.fetchone()['total']
        cur.execute("""
            SELECT classe_energetique, COUNT(*) as nb
            FROM resultat_calcul GROUP BY classe_energetique ORDER BY classe_energetique
        """)
        classes_data = cur.fetchall()
        cur.execute("SELECT AVG(consommation_kwh) as moy FROM resultat_calcul")
        row = cur.fetchone()
        stats['moyenne'] = round(row['moy'], 1) if row['moy'] else 0
        conn.close()
    return render_template('statistiques.html', stats=stats, classes_data=classes_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
