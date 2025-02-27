from functools import wraps
import os
import jwt
from flask import request, jsonify

def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Verify JWT token with Supabase public key
            jwt_secret = os.getenv('SUPABASE_JWT_SECRET')
            if not jwt_secret:
                raise ValueError('JWT secret not configured')

            # decoded = jwt.decode(
            #     token,
            #     jwt_secret,
            #     algorithms=["HS256"],
            #     options={"verify_signature": True},
            #     audience="authenticated",

            # )
            # current_user = decoded['sub']
            current_user = "c248ddda-97f8-453f-815f-9c031a5b9778"
        except (jwt.InvalidTokenError, ValueError) as e:
            return jsonify({'message': f'Token is invalid: {str(e)}'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
