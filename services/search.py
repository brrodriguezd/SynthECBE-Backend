from flask import request, jsonify
from instances import db, lm

def semantic_search(current_user):
    data = request.json
    if not data or 'query' not in data:
        return jsonify({'error': 'No search query provided'}), 400

    try:
        query_embedding = lm.model.encode(data['query']).tolist()
        print(query_embedding)
        threshold = data.get('threshold', 0.1)
        limit = data.get('limit', 5)

        response = db.db.rpc(
            'search_documents',
            {
                'query_embedding': query_embedding,
                'match_threshold': threshold,
                'match_count': limit
            }
        ).execute()

        return jsonify({'results': response.data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
