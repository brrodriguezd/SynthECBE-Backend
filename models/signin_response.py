from typing import Dict

def serialize_auth_response(auth_response) -> Dict:
    """
    Serializes a Supabase AuthResponse object into a JSON-serializable dictionary
    """
    return {
        'userid': auth_response.user.id,
        'email': auth_response.user.email,
        'role': auth_response.user.role,
        'access_token': auth_response.session.access_token if auth_response.session else None,
        'refresh_token': auth_response.session.refresh_token if auth_response.session else None,
        'expires_at': auth_response.session.expires_at if auth_response.session else None,
        'token_type': auth_response.session.token_type if auth_response.session else None
    }
