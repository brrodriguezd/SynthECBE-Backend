import services.documents as documents
from flask import Blueprint
from middleware.auth import verify_token

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/document/list', methods=['GET'])
@verify_token
def list_documents(current_user):
    return documents.list_documents(current_user)

@documents_bp.route('/documents/upload', methods=['POST'])
@verify_token
def upload_pdf(current_user):
    return documents.upload_pdf(current_user)
