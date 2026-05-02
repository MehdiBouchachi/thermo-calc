"""Route handlers for statistics."""

from flask import Blueprint
from app.controllers.calcul_controller import get_stats

bp = Blueprint('stats', __name__)

bp.add_url_rule('/statistiques', view_func=get_stats, methods=['GET'])
