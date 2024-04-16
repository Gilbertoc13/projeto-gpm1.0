from models.Midia import Midia
from middleware.all_middleware import verify_movie


def create_midia_controller(title, image_url, movie_type):
    movie_id = Midia.create_midia(title, image_url, movie_type)
    return {"id": movie_id, "message": f"Movie {title} created"}, 201

def get_all_movie_controller():
    return Midia.get_all_movie_ids()

def delete_movie_controller(movie_id):
    previous_movie_id = verify_movie(movie_id)
    if previous_movie_id:
        Midia.delete_movie(previous_movie_id, movie_id)
        return {"message": "Movie deleted"}


def update_movie_by_id_controller(movie_id, title):       
    verify_movie(movie_id)
    updated_fields = {"title": title}
    Midia.update_movie(movie_id, updated_fields)
    return {"message": "Movie updated successfully"}




    