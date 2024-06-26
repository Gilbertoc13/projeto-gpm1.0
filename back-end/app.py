from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from routes.user_routes import main_bp
from routes.tmdb_routes import tmdb_bp
from routes.media_routes import media_app
from routes.comment_routes import comment_app
import os
from pymongo import MongoClient
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

mongodb_uri = os.getenv("MONGODB_URI")
mongodb_dbname = os.getenv("MONGODB_DBNAME")

if mongodb_uri is None or mongodb_dbname is None:
    raise EnvironmentError("Variáveis de ambiente do MongoDB não estão definidas.")

client = MongoClient(mongodb_uri)
db = client.get_database(mongodb_dbname)
CORS(app)

app.register_blueprint(main_bp)
app.register_blueprint(tmdb_bp)
app.register_blueprint(media_app)
app.register_blueprint(comment_app)

if __name__ == "__main__":
    app.run(debug=True)
