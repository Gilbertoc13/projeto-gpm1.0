import os
from flask import request,jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.Comment import Comment
from flask import jsonify
from werkzeug.exceptions import BadRequest
from dotenv import load_dotenv
from models.Midia import Midia
load_dotenv()




comment_app = Blueprint("Comment_app", __name__)
user_tk = os.getenv('JWT_SECRET_KEY')





@comment_app.route('/api/comments/<media_id>/<comment_type>', methods=['POST'])
@jwt_required()
def add_comment(media_id, comment_type):
    user_id = get_jwt_identity()

    if not isinstance(media_id, str) or len(media_id) < 24:
        return jsonify({'message': 'Invalid media ID'}), 400

    
    movie = Midia.get_movie_by_id_model(media_id)
    if not movie:
        
        title = request.form.get('title')
        movie = Midia.create_midia(title=title, movie_type='')
    
    username = request.form.get('username')
    content = request.form.get('content')
    is_spoiler = request.form.get('isSpoiler', False)  

    try:
        comment_id = Comment.create_comment_evaluation_model(media_id, user_id, username, content, is_spoiler, comment_type)
        return jsonify({'message': 'Comment added successfully', 'comment_id': str(comment_id)}), 201
    except Exception as e:
        return jsonify({'message': 'Error adding comment'}), 500




@comment_app.route('/api/comments/<comment_id>', methods=['PUT'])
def update_comment_route(comment_id):
    try:
        
        updated_fields = request.json

        
        if not updated_fields:
            raise BadRequest("No updated fields provided in the request")

        
        success = Comment.update_comment(comment_id, updated_fields)

        if success:
            return jsonify({"message": "Comment updated successfully"}), 200
        else:
            return jsonify({"message": "Failed to update comment"}), 500

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": f"Unknown error: {str(e)}"}), 500
    

@comment_app.route('/api/comments/<comment_id>', methods=['DELETE'])
def delete_comment_route(comment_id):
    try:
        
        success = Comment.delete_comment(comment_id)

        if success:
            return jsonify({"message": "Comment deleted successfully"}), 200
        else:
            return jsonify({"message": "Failed to delete comment"}), 500

    except Exception as e:
        return jsonify({"error": f"Unknown error: {str(e)}"}), 500


@comment_app.route('/api/comments/<media_id>', methods=['GET'])
def get_comments(media_id):
    
    if not isinstance(media_id, str) or len(media_id) < 24:
        return jsonify({'message': 'Invalid media ID'}), 400

    try:
        comments = Comment.get_comment_by_id(media_id)
        return jsonify({'comments': comments}), 200
    except Exception as e:
        return jsonify({'message': 'Error retrieving comments'}), 500
