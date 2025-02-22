from middleware.auth import verify_token
import services.auth as auth
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    return auth.signup()

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    return auth.login()

@auth_bp.route('/auth/logout', methods=['POST'])
@verify_token
def logout():
    return auth.logout()
