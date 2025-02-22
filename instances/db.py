import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
db: Client
url: str| None = os.environ.get("SUPABASE_URL")
key: str| None = os.environ.get("SUPABASE_KEY")

if url and key:  db = create_client(url, key)
else:   raise Exception("No se encontraron las variables de entorno SUPABASE_URL y SUPABASE_KEY")
