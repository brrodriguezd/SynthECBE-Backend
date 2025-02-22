from flask import request, jsonify
from instances import db
from models.signin_response import serialize_auth_response

def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        response = db.db.auth.sign_in_with_password({
            "email": data['email'],
            "password": data['password']
        })
        res = serialize_auth_response(response)
        return jsonify(res)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def signup():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        response = db.db.auth.sign_up({
            "email": data['email'],
            "password": data['password']
        })
        return jsonify(serialize_auth_response(response))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def logout():
    try:
        db.db.auth.sign_out()

        return jsonify({
            'message': 'Successfully logged out',
            'status': 'success'
        }), 200

    except Exception as e:
        print(f"Logout error: {str(e)}")

        return jsonify({
            'error': 'Failed to logout',
            'message': str(e)
        }), 400
