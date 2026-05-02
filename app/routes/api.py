"""Route handlers for API endpoints."""

from flask import Blueprint
from app.controllers.composant_controller import add_mur, add_plancher, add_toiture, add_ouvrant
from app.controllers.calcul_controller import run_calcul

bp = Blueprint('api', __name__, url_prefix='/api')

bp.add_url_rule('/ajouter-mur', view_func=add_mur, methods=['POST'])
bp.add_url_rule('/ajouter-plancher', view_func=add_plancher, methods=['POST'])
bp.add_url_rule('/ajouter-toiture', view_func=add_toiture, methods=['POST'])
bp.add_url_rule('/ajouter-ouvrant', view_func=add_ouvrant, methods=['POST'])
bp.add_url_rule('/calculer/<int:batiment_id>', view_func=run_calcul, methods=['POST'])
