
import json
import os
from flask import make_response, request,jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.Midia import Midia
from models.User import User
from flask import jsonify
from werkzeug.exceptions import BadRequest 
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()


user_tk = os.getenv('JWT_SECRET_KEY')
midia_app = Blueprint("midia_app", __name__)

@midia_app.route('/api/media', methods=['POST'])
def create_midia():

    data = request.json()

    title = data['title']
    image_url = data['image_url']
    movie_type = data['movie_type']

    media_id = Midia.create_midia(title, image_url, movie_type)

    if media_id:
        return jsonify({'message': 'Media created successfully', 'media_id': media_id}), 201
    else:
        return jsonify({'message': 'Error creating media'}), 500



@midia_app.route('/api/users/<user_id>/watchlist/add', methods=['POST'])
@jwt_required()
def add_movie_to_watchlist(user_id):

    data = request.json()
    user_id = user_id


    movie_id = data['movie_id']

    response = User.add_movie_to_watchlist(user_id, movie_id)

    return jsonify(response), response['status_code']



@midia_app.route('/api/users/<user_id>/watchlist/delete', methods=['DELETE'])
@jwt_required()
def delete_movie_from_watchlist(user_id):
    user_id = user_id

    response = User.delete_movie_from_watchlist(user_id, None)  

    return jsonify(response), response['status_code']


@midia_app.route('/api/media/<media_id>/comments', methods=['GET'])
def get_media_comments(media_id):
    
    media_id = media_id

    comments = Midia.get_media_comments(media_id)

    if comments:
        return jsonify({'comments': comments}), 200
    else:
        return jsonify({'message': 'Media not found or comments not available'}), 404











 

       





