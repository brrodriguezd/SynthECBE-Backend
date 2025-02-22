from sentence_transformers import SentenceTransformer

# initialize language model

model = SentenceTransformer("nomic-ai/nomic-embed-text-v2-moe", trust_remote_code=True)
