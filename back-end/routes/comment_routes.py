import os
from flask import request,jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from pymongo import MongoClient
from models.Comment import Comment
from flask import jsonify
from dotenv import load_dotenv
from bson import json_util
load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))



comment_app = Blueprint("Comment_app", __name__)
user_tk = os.getenv('JWT_SECRET_KEY')





@comment_app.route("/api/comments", methods=["POST"])
@jwt_required()  
def create_comment_route():
    data = request.json
    tmdb_id = data.get("tmdb_id")
    comment = data.get("comment")
    is_spoiler = data.get("is_spoiler")

    if tmdb_id and comment is not None and is_spoiler is not None:
        comment_id = Comment.create_comment(tmdb_id, comment, is_spoiler)
        if comment_id:
            return jsonify({"message": "Comment created successfully", "comment_id": comment_id}), 201
        else:
            return jsonify({"message": "Failed to create comment"}), 500
    else:
        return jsonify({"message": "Missing tmdb_id, comment, or is_spoiler parameter"}), 400


@comment_app.route("/api/comments", methods=["GET"])
@jwt_required()  
def get_comments_by_user_route():
    try:
        user_email = get_jwt_identity()  
        comments_collection = db.comments
        comments = comments_collection.find({"user_id": user_email})

       
        comments = [json_util.dumps(comment) for comment in comments]

        return jsonify({"comments": comments}), 200
    except Exception as e:
        print(f"Error retrieving comments: {e}")
        return jsonify({"message": "Failed to retrieve comments"}), 500


@comment_app.route("/api/comments/<comment_id>", methods=["PUT"])
@jwt_required()  
def update_comment_route(comment_id):
    data = request.json
    comment = data.get("comment")
    is_spoiler = data.get("is_spoiler")

    if comment is not None and is_spoiler is not None:
        if Comment.update_comment(comment_id, comment, is_spoiler):
            return jsonify({"message": "Comment updated successfully"}), 200
        else:
            return jsonify({"message": "Failed to update comment"}), 500
    else:
        return jsonify({"message": "Missing comment or is_spoiler parameter"}), 400

@comment_app.route("/api/comments/<comment_id>", methods=["DELETE"])
@jwt_required()  
def delete_comment_route(comment_id):
    if Comment.delete_comment(comment_id):
        return jsonify({"message": "Comment deleted successfully"}), 200
    else:
        return jsonify({"message": "Failed to delete comment"}), 500


