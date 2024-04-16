
from flask import make_response, request,jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.Movie import Movie
from models.User import User
from flask import jsonify
from werkzeug.exceptions import BadRequest 
from bson import ObjectId


movie_app = Blueprint("movie_app", __name__)

@movie_app.route('/api/media/<media_type>', methods=['POST'])
def create_media(media_type):
    try:
        data = request.get_json()
        if data is None:
            raise BadRequest("Missing request data (expected JSON)")

        title = data.get("title")
        image_url = data.get("image_url", "")
        comments = data.get("comments", [])

        if not all([title]):
            raise BadRequest("Missing required fields: title")

        media = {
            "title": title,
            "image_url": image_url,
            "type": media_type,
            "content": {"comments": comments}
        }

        existing_media = Movie.get_movie_by_title(title)
        if existing_media:
            existing_media['_id'] = str(existing_media['_id'])
            return jsonify({"message": f"Media '{title}' already exists", "data": existing_media}), 200
        else:
            new_media_id = Movie.create_content(media)
            return jsonify({"message": "Media created successfully", "_id": new_media_id}), 201

    except BadRequest as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        print(f"Error creating media: {e}")
        return jsonify({"message": "Internal server error"}), 500


@movie_app.route('/api/user/movies/<user_id>', methods=['GET'])
def get_user_movies(user_id):
    try:
      
        if not user_id or not isinstance(user_id, str):
            raise BadRequest("Invalid user ID")

        
        user_movies = User.get_user_movie_list(user_id)

        
        if not user_movies:
            return jsonify({"message": "No movies found in the user's list"}), 404

        
        return jsonify({"user_movies": user_movies}), 200

    except BadRequest as e:
        return make_response(jsonify({"error": str(e)}), 400)

    except Exception as e:
        return make_response(jsonify({"error": f"Unknown error: {str(e)}"}), 500)



def add_to_watchlist(media_type, media_id, user_id):

    
    if not isinstance(media_id, str) or len(media_id) < 24:
        return jsonify({'message': 'Invalid media ID'}), 400


    if media_type == 'movies':
        media_data = Movie.get_movie_by_id_model({'_id': ObjectId(media_id)})
        if not media_data:
            return jsonify({'message': 'Media not found'}), 404

    
    User.update_user({'_id': ObjectId(user_id)}, {'$push': {'watched_movies': media_id}})

    return jsonify({'message': 'Media added to watchlist successfully'}), 200


@movie_app.route('/api/watchlist/<media_type>/<media_id>', methods=['POST'])
@jwt_required()
def add_to_watchlist(media_type, media_id):
    
    user_id = get_jwt_identity()

    if media_type not in ['movies', 'series']:
        return jsonify({'message': 'Invalid media type'}), 400

    
    if not isinstance(media_id, str) or len(media_id) < 24:
        return jsonify({'message': 'Invalid media ID'}), 400

    

    add_to_watchlist(media_type, media_id, user_id)

    
    return jsonify({'message': 'Media added to watchlist successfully'}), 200

@movie_app.route('/api/user/movies/<movie_id>', methods=['DELETE'])
def delete_movie_from_user_list(movie_id):
    try:
        
        user_id = request.json.get('user_id')

        
        if not user_id or not isinstance(user_id, str):
            raise BadRequest("Invalid user ID")

        
        if not User.get_user_movie_list(user_id, movie_id):
            return jsonify({"message": "Movie not found in user's list"}), 404

       
        success = User.remove_movie_from_list(user_id, movie_id)

        if success:

            
            User.remove_movie_from_watched_movies(user_id, movie_id)

            return jsonify({"message": "Movie removed from user's list successfully"}), 200
        else:
            return jsonify({"message": "Failed to remove movie from user's list"}), 500

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": f"Unknown error: {str(e)}"}), 500








 

       




