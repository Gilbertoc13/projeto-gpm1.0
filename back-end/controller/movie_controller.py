from models.Content import Movie
from bson import ObjectId
from middleware.all_middleware import verify_movie


def create_movie_and_tv(title, image_url, movie_type):
    movie_id = Movie.create_movie_and_tv(title, image_url, movie_type)
    return {"id": movie_id, "message": f"Movie {title} created"}, 201

def get_all_movie_controller():
    return Movie.get_all_movie_ids()

def delete_movie_controller(movie_id):
    previous_movie_id = verify_movie(movie_id)
    if previous_movie_id:
        Movie.delete_movie(previous_movie_id, movie_id)
        return {"message": "Movie deleted"}


def update_movie_by_id_controller(movie_id, title):       
    verify_movie(movie_id)
    updated_fields = {"title": title}
    Movie.update_movie(movie_id, updated_fields)
    return {"message": "Movie updated successfully"}


    