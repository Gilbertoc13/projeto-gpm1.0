from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))
class User:

    @staticmethod
    def create_user_model(email,username, hashed_password_base64):
        users_collection = db.users
        new_user = {
            "username": username,
            "email": email,
            "password": hashed_password_base64,
            "movie_list": [],
            "watched_movies": []
        }
        result = users_collection.insert_one(new_user)
        return str(result.inserted_id)

    @staticmethod
    def get_user_by_username_model(username):
        users_collection = db.users
        user = users_collection.find_one({"username": username})
        return user
    
    @staticmethod
    def get_user_by_email_model(email):
        users_collection = db.users
        user = users_collection.find_one({"email": email})
        return user
    
    @staticmethod
    def get_user_by_id_model(id):
        users_collection = db.users
        user = users_collection.find_one({"_id": ObjectId(id)})
        return user
    
    @staticmethod
    def update_user(user_id, updated_fields):
        users_collection = db.users
        result = users_collection.update_many({"_id": ObjectId(user_id)}, {"$set": updated_fields})
        return result
    
    @staticmethod
    def get_followers_model(user_id):
        users_collection = db.users
        followers = users_collection.find({"following": user_id})
        return list(followers)
    
    @staticmethod
    def delete_account_model(user_id):
        users_collection = db.users
        result = users_collection.find_one_and_delete({"_id": ObjectId(user_id)})
        return result
    
    @staticmethod
    def get_user_movie_list(user_id):
        user = User.get_user_by_id_model(user_id)
        if user:
            return user.get('movie_list', [])
        else:
            return None
        
    @staticmethod
    def remove_movie_from_list(user_id, movie_id):
        try:
            users_collection = db.users
            result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$pull": {"movie_details": movie_id}})
            return result.modified_count > 0
        except Exception as e:
            print(f"Error deleting movie details from user: {e}")
            return False

    @staticmethod
    def remove_movie_from_watched_movies(user_id, movie_id):
        try:
            users_collection = db.users
            result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$pull": {"watched_movies": movie_id}})
            return result.modified_count > 0
        except Exception as e:
            print(f"Error removing movie from watched movies of user: {e}")
            return False
        
 
  
        
    
    
    