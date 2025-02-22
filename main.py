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


if __name__ == '__main__':
    app.run(debug=True)
