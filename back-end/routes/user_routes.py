
import os
from dotenv import load_dotenv
from flask import request,jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from pymongo import MongoClient
from controller.user_controller import login, create_user_controller, get_user_data
from models.Media import MediaAPI
from models.User import User
from flask import jsonify

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))

api_key = os.getenv('TMDB_KEY')
main_bp = Blueprint("main_bp", __name__)

@main_bp.route("/api/login", methods=["POST"])
def login_route():
    data = request.get_json()
    if "email" not in data or "password" not in data:
        return jsonify({"message": "Faltando email ou senha!"}), 400

    email = data["email"]
    password = data["password"]

    response, status_code = login(email, password)
    return jsonify(response), status_code

@main_bp.route("/api/cadastro", methods=["POST"])
def create_user_route():
    data = request.get_json()
    if not all(key in data for key in ["username", "email", "password"]):
        return jsonify({"message": "Missing required fields"}), 400


    username = data["username"]
    email = data["email"]
    password = data["password"]

    response, status_code = create_user_controller(email, username, password)
    print(response)
    return jsonify(response), status_code

@main_bp.route('/api/data_user', methods=['GET'])
@jwt_required()
def data_user_route():
    return get_user_data()
    
@main_bp.route('/api/user_name', methods=['GET'])
@jwt_required()
def get_user_name():
    user_email = get_jwt_identity()
    user = User.get_user_by_email_model(user_email)
    if user:
        return jsonify({"user": user.get("username", "Unknown")}), 200
    else:
        return jsonify({"message": "User not found"}), 404

@main_bp.route('/api/user/watched', methods=['GET'])
@jwt_required()
def get_watched_list():
    try:
        user_id = get_jwt_identity()
        user = User.get_user_by_id_model(user_id)
        if user:
            watched_list = user.get("watched", []) 
            return jsonify({"watched_media": watched_list}), 200
        else:
            return jsonify({"error": "User not found."}), 404
    except Exception as e:
        print(f"Error retrieving watched list: {e}")
        return jsonify({"error": "Failed to retrieve watched list."}), 500

@main_bp.route('/api/user/watched', methods=['DELETE'])
@jwt_required() 
def delete_from_watched_list_route():
    try:
        data = request.json
        tmdb_id = data.get('tmdb_id')
        media_type = data.get('media_type')

        if not tmdb_id:
            return jsonify({"error": "Missing 'tmdb_id' parameter"}), 400
        if not media_type:
            return jsonify({"error": "Missing 'media_type' parameter"}), 400

        if User.delete_from_watched_list(tmdb_id, media_type, api_key):
            return jsonify({"message": "Media removed from watched list successfully"}), 200
        else:
            return jsonify({"error": "Failed to remove media from watched list"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@main_bp.route('/api/user/watched', methods=['POST'])
@jwt_required() 
def add_watched_list_route():
    try:
        data = request.json
        tmdb_id = data.get('tmdb_id')
        media_type = data.get('media_type')

        if not tmdb_id or not media_type:
            return jsonify({"error": "Missing parameters"}), 400

        if User.add_watched_list(tmdb_id, media_type, api_key):
            return jsonify({"message": "Media added to watched list successfully"}), 200
        else:
            return jsonify({"error": "Failed to add media to watched list"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@main_bp.route("/api/user/media/seen", methods=["GET"])
@jwt_required()
def verify_media_seen():
    try:
        user_id = get_jwt_identity()
        media_id = request.args.get("id")
        media_type = request.args.get("type")

        if not media_id or not media_type:
            return jsonify({"error": "Missing parameters 'id' and/or 'type'"}), 400

        user = User.get_user_by_id_model(user_id)

        if user:
            watched_list = user.get("watched", [])

            for media in watched_list:
                if media.get("tmdb_id") == media_id and media.get("media_type") == media_type:
                    return jsonify({"seen": True}), 200

            return jsonify({"seen": False}), 200
        else:
            return jsonify({"error": "User not found."}), 404
    except Exception as e:
        print(f"Error checking if media is watched: {e}")
        return jsonify({"error": "Failed to check if media is watched."}), 500