
from flask import request,jsonify, Blueprint
from flask_jwt_extended import jwt_required
from controller.user_controller import login, create_user_controller, get_user_data
from models.User import User
from flask import jsonify




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
    return jsonify(response), status_code


@main_bp.route('/api/data_user', methods=['GET'])
@jwt_required()
def data_user_route():
    return get_user_data()


