from flask import Blueprint

calculation = Blueprint('calculation', __name__, url_prefix='/calculation')

from . import views