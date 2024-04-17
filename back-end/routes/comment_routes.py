import os
from flask import request,jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.Comment import Comment
from flask import jsonify
from dotenv import load_dotenv
load_dotenv()




comment_app = Blueprint("Comment_app", __name__)
user_tk = os.getenv('JWT_SECRET_KEY')





@comment_app.route('/api/comments', methods=['POST'])
@jwt_required()
def create_comment():
    user_id = get_jwt_identity()
    data = request.json() 


    tmdb_id = data['tmdb_id']
    comment = data['comment',[]]
    is_spoiler = data['isSpoiler', False] 
    
    comment_id = Comment.create_comment(user_id, tmdb_id, comment, is_spoiler)

    if comment_id:
        return jsonify({'message': 'Comment created successfully', 'comment_id': comment_id}), 201
    else:
        return jsonify({'message': 'Error creating comment'}), 500




@comment_app.route('/api/comments/<comments_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):

    data = request.json()
    
    new_comment= data['comment',[]]
    is_spoiler = data['isSpoiler', False] 

    update_success = Comment.update_comment(comment_id, new_comment, is_spoiler)

    if update_success:
        return jsonify({'message': 'Comment updated successfully'}), 200
    else:
        return jsonify({'message': 'Error updating comment'}), 500


@comment_app.route('/api/comments/<comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    
    delete_success = Comment.delete_comment(comment_id)

    if delete_success:
        return jsonify({'message': 'Comment deleted successfully'}), 200
    else:
        return jsonify({'message': 'Error deleting comment'}), 500

@comment_app.route('/api/comments/<user_id>', methods=['GET'])
@jwt_required()
def get_comments_by_user(user_id):
    comments = Comment.get_comments_by_user(user_id)
    if comments:
        return jsonify({'comments': [comment for comment in comments]})
    else:
        return jsonify({'message': 'No comments found'}), 404

    


