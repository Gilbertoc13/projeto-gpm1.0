
from flask import request,jsonify, Blueprint
from controller.Movie_Tv_controller import create_media
from controller.user_controller import login, create_user_controller
from models.Movies_TV import Movie
from models.User import User


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

@main_bp.route("/api/test", methods=["GET"])
def test_route():
    return jsonify({"message": "API funcionando!"})



@main_bp.route('/api/media/<media_type>/<media_id>', methods=['POST'])
def get_or_create_media(media_type, media_id=None, title=None, director= None, release_year= None):

    #apenas para ser testado no Thunder Client. (Pode excluir depois).
    if title == None and director == None and release_year == None:
        data = request.json
        title = data.get('title')
        director = data.get('director')
        release_year = data.get('release_year')
        
    if media_type not in ['movie', 'tv']:
        return jsonify({'message': 'Invalid media type'}), 400
    

    if media_type == 'movie':
        media = Movie.get_movie_by_id_model(media_id, movie_type='movie')


    if media:
        return jsonify(media), 200
    elif media_id  == None:
        new_media = create_media(media_type, media_id, title, director, release_year)
        if new_media:
            return jsonify(new_media), 201
        else:
            return jsonify({'message': 'Failed to create media'}), 500
        

@main_bp.route('/api/movies', methods=['GET'])
def get_movies():
    movie_ids = Movie.get_all_movie_ids()

    movies_data = []  

    for movie_id in movie_ids:
        movie = Movie.get_movie_by_id_model(movie_id, movie_type="movie")  

        if movie:  
            movie["_id"] = str(movie["_id"])  
            movies_data.append(movie)

    return jsonify(movies_data), 200


@main_bp.route('/api/movies/<movie_id>/watched', methods=['POST'])
def mark_watch(movie_id):
    movie_type = request.args.get('movie_type', 'movie')  

    result = Movie.mark_movie_as_watched(movie_id, movie_type="")

    if result:
        return jsonify({'message': 'Movie marked as watched'}), 200
    else:
        return jsonify({'message': 'Movie not found or type invalid'}), 404


