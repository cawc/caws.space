from flask import Blueprint

bp = Blueprint('idea', __name__)

from app.idea import routes