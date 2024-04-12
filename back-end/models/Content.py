
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv


load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))

class Movie:
    @staticmethod
    def create_content(title, image_url, movie_type):
      movies_collection = db.movies
      new_movie = {
        "title": title,
        "type": movie_type,  
        "image_url": image_url,
        "comments": []
    }
      result = movies_collection.insert_one(new_movie)
      return {
        "title": title,
        "id": str(result.inserted_id),  
        "type": movie_type,
        "comment": []
    }

    @staticmethod
    def get_all_movie_ids():
        movies_collection = db.movies
        movie_ids = [movie['_id'] for movie in movies_collection.find()] 
        return movie_ids


    @staticmethod
    def get_movie_by_title(title, movie_type):
        movies_collection = db.movies
        movie = movies_collection.find_one({"title": title, "type": movie_type})
        return movie

    @staticmethod
    def get_movie_by_id_model(movie_id, movie_type="movie"):
      movies_collection = db.movies
      movie = movies_collection.find_one(
        {"_id": movie_id, "type": movie_type}, projection={"title": 1, "image_url": 1}
    )
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
    def validate_movie_type(movie_type):
       valid_types = ["movie", "tv"]
       return movie_type.lower() in valid_types
    
    @staticmethod
    def mark_movie_as_watched(movie_id):
     try:
        result = Movie.update_movie_watched_status(movie_id, watched=True)
        return result
     except Exception as e:
        print(f"Error marking movie as watched: {e}")
        return False

    @staticmethod
    def update_movie_watched_status(movie_id, watched=True):
     
     try:
      movie_id = ObjectId(movie_id) 
      db.movies.update_one({"_id": movie_id}, {"$set": {"watched": watched}})
      return True
    
     except Exception as e:
      print(f"Error updating movie watched status: {e}")
      return False
    

 
    
  
