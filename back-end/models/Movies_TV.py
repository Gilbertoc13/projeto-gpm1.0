
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))

class Movie:
    @staticmethod
    def create_movie_and_tv(title, director, release_year, movie_type=None):
      movies_collection = db.movies
      new_movie = {
        "title": title,
        "director": director,
        "release_year": release_year,
        "type": movie_type,  
    }
      result = movies_collection.insert_one(new_movie)
      return {
        "title": title,
        "id": str(result.inserted_id),  
        "type": movie_type,
    }

    @staticmethod
    def get_all_movie_ids():
        movies_collection = db.movies
        movie_ids = [movie['_id'] for movie in movies_collection.find()] 
        return movie_ids


    @staticmethod
    def get_movie_by_title(title):
        movies_collection = db.movies
        movie = movies_collection.find_one({"title": title})
        return movie

    @staticmethod
    def get_movie_by_id_model(movie_id, movie_type="movie"):
        movies_collection = db.movies
        movie = movies_collection.find_one({"_id": ObjectId(movie_id), "type": movie_type})
        return movie

    @staticmethod
    def update_movie(movie_id, updated_fields):
        movies_collection = db.movies
        result = movies_collection.update_many({"_id": ObjectId(movie_id)}, {"$set": updated_fields})
        return result

    @staticmethod
    def delete_movie(movie_id):
        movies_collection = db.movies
        result = movies_collection.find_one_and_delete({"_id": ObjectId(movie_id)})
        return result
    
    @staticmethod
    def mark_movie_as_watched(movie_id, movie_type='movie'):
       movie = Movie.get_movie_by_id_model(movie_id)
       if movie_type != 'movie':
          return False
       else:
          movies_collection = db.movies
          movies_collection.update_one({'_id': movie_id}, {'$set': {'watched': True}}, upsert=True)  # Using upsert=True

          return True
    

 
    
  
