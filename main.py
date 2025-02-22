from flask import Flask
from dotenv import load_dotenv
from routes.auth import auth_bp
from routes.documents import documents_bp
from routes.search import search_bp

# load environment variables
load_dotenv()

#initialize app
app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(documents_bp)
app.register_blueprint(search_bp)

# 16 MB por archivo
app.config['MAX_CONTENT_LENGHT'] = 16 * 1024 * 1024
# 50 MB por formulario
app.config['MAX_FORM_MEMORY_SIZE'] = 50 * 1024 * 1024


if __name__ == '__main__':
    app.run(debug=True)
