
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import requests



load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))
api_key= os.getenv('TMDB_KEY')





class MediaAPI:
    @staticmethod
    def get_media_details(tmdb_id, media_type, api_key):
        base_url = "https://api.themoviedb.org/3/"
        url = f"{base_url}{media_type}/{tmdb_id}?api_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data.")
            return None

    @staticmethod
    def add_media_to_database(media_details, db):
        if media_details:
            media_data = {
                "tmdb_id": media_details["id"],  # Ajuste para "id" em vez de "tmdb_id"
                "backdrop_path": media_details["backdrop_path"],
                "title": media_details["title"],
                "vote_average": media_details["vote_average"],
                "release_date": media_details["release_date"]
            }
            collection = db["media"]
            result = collection.insert_one(media_data)
            print("Media added to database successfully.")
            return str(result.inserted_id)
        else:
            print("Failed to add media to database.")
            return None
    
    @staticmethod
    def get_or_create_media(tmdb_id, media_type,db, api_key):  
        collection = db["media"]
        existing_media = collection.find_one({"tmdb_id": tmdb_id})  
        if existing_media:
            print("Media already exists in database.")
            return existing_media["_id"]
        else:
            media_details = MediaAPI.get_media_details(tmdb_id, media_type, api_key)
            if media_details:
                return MediaAPI.add_media_to_database(media_details, db)
            else:
                return None
