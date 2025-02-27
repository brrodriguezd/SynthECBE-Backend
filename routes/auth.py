from middleware.auth import verify_token
import services.auth as auth
from flask import Blueprint, request, make_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    if request.method == 'OPTIONS':
        # Create a blank response for the preflight request
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        return response, 200

    return auth.signup()

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'OPTIONS':
        # Create a blank response for the preflight request
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        return response, 200
    return auth.login()

@auth_bp.route('/auth/logout', methods=['POST'])
@verify_token
def logout():
    if request.method == 'OPTIONS':
        # Create a blank response for the preflight request
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        return response, 200

    return auth.logout()
