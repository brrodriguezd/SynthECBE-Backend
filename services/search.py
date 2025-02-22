from flask import jsonify
from instances import db, lm

def search(current_user, query, threshold = 0.7, limit=5):
    try:
        results_normal = normal_search(current_user, query, limit)
        results_semantic = semantic_search(current_user, query, threshold, limit)
        results = merge_and_sort_results(results_normal, results_semantic)
        return jsonify({
            "results": results
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def merge_and_sort_results(fuzzy_results, semantic_results):
    """
    Merges fuzzy and semantic search results, removes duplicates based on document ID,
    and sorts the final list in descending order by similarity.

    Assumptions:
      - fuzzy_results: list of dicts with key 'id' and 'similarity'
      - semantic_results: list of dicts with key 'document_id' and 'similarity'

    Duplicate documents (same document id) are determined by comparing fuzzy's 'id'
    and semantic's 'document_id'. If a document appears in both, the one with the higher
    similarity score is retained.
    """
    combined = {}

    # Process fuzzy search results (using 'id' as the unique key)
    for item in fuzzy_results:
        doc_id = item.get("id")
        if doc_id:
            # Store item if it's the first time, or if its similarity is higher than an existing one
            if doc_id not in combined or combined[doc_id]["similarity"] < item["similarity"]:
                combined[doc_id] = item

    # Process semantic search results (using 'document_id' as the unique key)
    for item in semantic_results:
        doc_id = item.get("document_id")
        if doc_id:
            # Use document_id as key and choose the one with the higher similarity
            if doc_id not in combined or combined[doc_id]["similarity"] < item["similarity"]:
                combined[doc_id] = item

    # Convert the dictionary back to a list and sort by similarity (descending)
    merged_list = list(combined.values())
    merged_list.sort(key=lambda x: x["similarity"], reverse=True)
    return merged_list
def normal_search(current_user, query ,limit):
    try:
        response = db.db.rpc(
                "fuzzy_search_documents",
                {"search_query": query.upper(), "match_count": limit}
            ).execute()
        return response.data if response.data else []
    except Exception as e:
        raise e

def semantic_search(current_user, query, threshold, limit):
    try:
        query_embedding = lm.model.encode(query).tolist()

        response = db.db.rpc(
            'search_documents',
            {
                'query_embedding': query_embedding,
                'match_threshold': threshold,
                'match_count': limit
            }
        ).execute()

        return response.data if response.data else []

    except Exception as e:
        raise e
