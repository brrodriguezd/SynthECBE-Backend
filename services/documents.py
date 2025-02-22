from flask import request, jsonify
from services.process import process_pdf
from typing import List, Dict
import numpy as np
from instances import lm, db
from uuid import uuid4

pdf_chunks: List[Dict] = []
embeddings: List[np.ndarray] = []
def upload_pdf(current_user):
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename is None or not file.filename.endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400


    document_id = str(uuid4())
    try:
        document_data = {
            'id': document_id,
            'uploaded_by': current_user,
            'filename': file.filename,
            'status': 'processing'
        }

        db.db.table('documents').insert(document_data).execute()
        print(document_data)

        chunks = process_pdf(file.read())

        for idx, chunk in enumerate(chunks):
            embedding = lm.model.encode(chunk).tolist()
            print(embedding)
            chunk_data = {
                'document_id': document_id,
                'chunk_index': idx,
                'content': chunk,
                'embedding': embedding
            }
            db.db.table('document_chunks').insert(chunk_data).execute()

        # Update status
        db.db.table('documents').update({
            'status': 'completed'
        }).eq('id', document_id).execute()

        return jsonify({
            'message': 'PDF processed successfully',
            'document_id': document_id,
            'chunks_processed': len(chunks)
        })

    except Exception as e:
        if document_id:
            db.db.table('documents').update({
                'status': 'error',
                'error_message': str(e)
            }).eq('id', document_id).execute()

        return jsonify({'error': str(e)}), 500

# Update the table references in the backend code
def list_documents(current_user):
    try:
        response = db.db.table('documents')\
            .select('id, filename, status, created_at, updated_at, uploaded_by')\
            .execute()

        return jsonify({'documents': response.data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def upload_file(path: str, filename: str):
    try:
        # Test query
        test = db.db.table('documents').select('*').limit(1).execute()
        print("Connection successful:", test.data)
    except Exception as e:
        print("Connection error:", str(e))
    document_id = str(uuid4())
    try:
        document_data = {
            'id': document_id,
            'uploaded_by': 'c248ddda-97f8-453f-815f-9c031a5b9778',
            'filename': filename,
            'status': 'processing'
        }
        db.db.table('documents').insert(document_data).execute()

        chunks = process_pdf(path)

        for idx, chunk in enumerate(chunks):
            embedding = lm.model.encode(chunk).tolist()
            chunk_data = {
                'document_id': document_id,
                'chunk_index': idx,
                'content': chunk,
                'embedding': embedding
            }
            db.db.table('document_chunks').insert(chunk_data).execute()

        # Update status
        db.db.table('documents').update({
            'status': 'completed'
        }).eq('id', document_id).execute()

        return 'message PDF processed successfully,'+ 'document_id: '+ str(document_id)+'chunks_processed: '+ str(len(chunks))

    except Exception as e:
        if document_id:
            db.db.table('documents').update({
                'status': 'error',
                'error_message': str(e)
            }).eq('id', document_id).execute()

        raise Exception ('error'+ str(e))
