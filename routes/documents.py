import services.documents as documents
from flask import Blueprint, request, make_response
from middleware.auth import verify_token

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/documents/list', methods=['GET'])
@verify_token
def list_documents(current_user):
    return documents.list_documents(current_user)

@documents_bp.route('/documents/upload', methods=['POST'])
@verify_token
def upload_pdf(current_user):
    if request.method == 'OPTIONS':
        # Create a blank response for the preflight request
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        return response, 200
    return documents.upload_pdf(current_user)
