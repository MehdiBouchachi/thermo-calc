"""Route handlers for batiment (building) management."""

from flask import Blueprint
from app.controllers.batiment_controller import (
    list_batiments, create_batiment, detail_batiment, delete_batiment
)

bp = Blueprint('batiments', __name__)

bp.add_url_rule('/', view_func=list_batiments, methods=['GET'])
bp.add_url_rule('/batiment/nouveau', view_func=create_batiment, methods=['GET', 'POST'])
bp.add_url_rule('/batiment/<int:batiment_id>', view_func=detail_batiment, methods=['GET'])
bp.add_url_rule('/batiment/<int:batiment_id>/supprimer', view_func=delete_batiment, methods=['POST'])
