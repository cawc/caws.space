from app import login
from app.models import User
from functools import wraps

from flask import current_app
from flask_login import current_user

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def admin_required(func):
    """
    Decorator to make sure that is_admin is set to True on the current_user object.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return func(*args, **kwargs)
        return current_app.login_manager.unauthorized()
    return decorated_view 
