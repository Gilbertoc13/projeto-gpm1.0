from models.Movies_TV import Movie

def create_media(media_type, media_id, title, director, release_year):
    if media_type == 'movie':
        new_movie_id = Movie.create_movie_and_tv(title, director, release_year)
        new_movie = {
            'title': title,
            'director': director,
            'release_year': release_year,
            '_id': new_movie_id
        }
        return new_movie
    elif media_type == 'tv':
        new_tv_id = Movie.create_movie_and_tv(title, director, release_year)
        new_tv = {
            'title': title,
            'director': director,
            'release_year': release_year,
            '_id': new_tv_id
        }
        return new_tv
    else:
        return None
