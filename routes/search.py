import services.search as search
from flask import Blueprint
from middleware.auth import verify_token

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['POST'])
@verify_token
def semantic_search(current_user):
    return search.semantic_search(current_user)
