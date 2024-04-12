
from flask import request,jsonify, Blueprint
from flask_jwt_extended import jwt_required
from models.Content import Movie
from models.User import User
from flask import jsonify
from werkzeug.exceptions import BadRequest 
from controller.user_controller import get_user_data


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


 

       

@movie_app.route('/api/movies', methods=['GET'])
@jwt_required()
def get_movies():
    try:
        user_id = get_user_data()

        if not user_id:
            return jsonify({"message": "User not authenticated"}), 401

        
        watched_movies = User.get_user_movie_list(user_id)  

        if not watched_movies:
            return jsonify({"message": "No movies found in your watched list"}), 404

        
        movies_data = []
        for movie_id in watched_movies:
            movie = Movie.get_movie_by_id_model(movie_id)
            if movie:
                
                movie["_id"] = str(movie["_id"])  
                movies_data.append(movie)

        return jsonify(movies_data), 200

    except Exception as e:
        print(f"Error getting movies: {e}")
        return jsonify({"message": "Internal server error"}), 500




@movie_app.route('/api/movies/<movie_id>/watched', methods=['POST'])
@jwt_required()
def mark_watched_route(movie_id):
    try:
        user_id = get_user_data()
        
        if not user_id:
            return jsonify({"message": "User not authenticated"}), 401
        
        movie = Movie.get_movie_by_id_model(movie_id)
        if not movie:
            return jsonify({"message": "Movie not found"}), 404
        
        user = User.get_user_movie_list(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        user = User.add_watched_movie(movie_id)
        
        return jsonify({"message": "Movie marked as watched for the user"}), 200
    
    except Exception as e:
        print(f"Error marking movie as watched: {e}")
        return jsonify({"message": "Internal server error"}), 500






