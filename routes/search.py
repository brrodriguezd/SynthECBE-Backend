import services.search as search_service
from flask import Blueprint, request, jsonify
from middleware.auth import verify_token

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['POST'])
@verify_token
def search(current_user):
    data = request.json
    if not data or 'query' not in data:
        return jsonify({'error': 'No search query provided'}), 400
    return search_service.search(current_user, data.get('query'), data.get('threshold'), data.get('limit'))
