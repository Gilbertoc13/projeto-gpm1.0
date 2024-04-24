import os
from flask import request,jsonify, Blueprint
from flask_jwt_extended import jwt_required
from pymongo import MongoClient
from models.Comment import Comment
from models.Media import MediaAPI
from flask import jsonify
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))



comment_app = Blueprint("Comment_app", __name__)
user_tk = os.getenv('JWT_SECRET_KEY')
api_key = os.getenv('TMDB_KEY')





@comment_app.route("/api/comment", methods=["POST"])
@jwt_required()
def create_comment_route():
        data = request.json
        tmdb_id = data.get("tmdb_id")
        media_type = data.get("media_type")
        review = data.get("review")  
        is_spoiler = data.get("is_spoiler")
        stars = data.get("stars")

        if not all([tmdb_id, media_type, review, is_spoiler, stars]):
            return jsonify({"error": "Missing parameters"}), 400

        comment_id = (Comment.create_comment(tmdb_id, media_type, review, is_spoiler, stars))
        if comment_id:
            return jsonify({"message": "Comment created successfully", "comment_id": comment_id}), 201
        else:
            return jsonify({"error": "Failed to create comment"}), 500


@comment_app.route("/api/comment/user", methods=["GET"])
@jwt_required()
def get_comments_by_user_route():
    try:
        return Comment.get_comments_by_user()
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



@comment_app.route("/api/comment", methods=["GET"])
@jwt_required()
def get_media_with_comments_route():
    try:
        media_with_comments = MediaAPI.get_all_media_comments()
        if media_with_comments:
            return jsonify({"media_with_comments": media_with_comments}), 200
        else:
            return jsonify({"error": "Failed to retrieve media with comments"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    

@comment_app.route("/api/comment/<tmdb_id>/<media_type>", methods=["GET"])
def get_media_comment_route(tmdb_id, media_type):
    try:
        media = MediaAPI.get_media_comment(tmdb_id, media_type)
        if media:
            return jsonify({"comment": media}), 200
        else:
            return jsonify({"error": "comment not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500




@comment_app.route("/api/comment/<comment_id>", methods=["PUT"])
@jwt_required()
def update_comment_route(comment_id):
    try:
        data = request.json
        review = data.get("review")
        is_spoiler = data.get("is_spoiler")
        stars = data.get("stars")

        if not all([review, is_spoiler, stars]):
            return jsonify({"error": "Missing parameters"}), 400

        if Comment.update_comment(comment_id, review, is_spoiler, stars):
            return jsonify({"message": "Comment updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update comment"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



@comment_app.route("/api/comment/<comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment_route(comment_id):
    try:
        if Comment.delete_comment(comment_id):
            return jsonify({"message": "Comment deleted successfully"}), 200
        else:
            return jsonify({"error": "Failed to delete comment"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

