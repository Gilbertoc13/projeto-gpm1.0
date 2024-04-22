
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
        url = f"{base_url}{media_type}/{tmdb_id}?api_key={api_key}&language=pt-BR"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data.")
            return None

    @staticmethod
    def add_media_to_database(media_details, media_type, db):
        if media_details:
            if(media_type == "movie"):
                media_data = {
                    "tmdb_id": media_details["id"],  
                    "poster_path": media_details["poster_path"] or '',
                    "title": media_details["title"] or media_details["name"],
                    "vote_average": media_details["vote_average"] or '?',
                    "release_date": media_details["release_date"] or media_details["first_air_date"],
                    "media_type": media_type,
                    "comments": []
                }
            else:
                media_data = {
                "tmdb_id": media_details["id"],  
                "poster_path": media_details["poster_path"] or '',
                "title": media_details["name"],
                "vote_average": media_details["vote_average"] or '?',
                "release_date": media_details["first_air_date"],
                "media_type": media_type,
                "comments": []
                }
            collection = db["media"]
            result = collection.insert_one(media_data)
            print("Media added to database successfully.")
            return result
        else:
            print("Failed to add media to database.")
            return None

    
    @staticmethod
    def get_or_create_media(tmdb_id, media_type, api_key):  
        collection = db["media"]
        existing_media = collection.find_one({"tmdb_id": int(tmdb_id), "media_type": media_type})  
        if existing_media:
            print("Media already exists in database.")
            return existing_media
        else:
            media_details = MediaAPI.get_media_details(tmdb_id, media_type, api_key)
            if media_details:
                MediaAPI.add_media_to_database(media_details, media_type, db)
                return media_details
            else:
                return None


    @staticmethod
    def get_media_comments(tmdb_id, db):
        collection = db["media"]
        media = collection.find_one({"tmdb_id": tmdb_id}, {"comments": 1})
        if media:
            comments = media.get("comments", [])
            return comments
        else:
            print("Media not found in the database.")
            return None

    @staticmethod
    def get_all_media(db):
        collection = db["media"]
        all_media = collection.find({}, {"_id": 0}) 
        return list(all_media)
