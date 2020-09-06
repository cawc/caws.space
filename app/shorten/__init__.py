from flask import Blueprint

bp = Blueprint('shorten', __name__)

from app.shorten import routes