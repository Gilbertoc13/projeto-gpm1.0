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
            "midia_list": [],
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
    def get_user_midia_list(user_id):
        user = User.get_user_by_id_model(user_id)
        if user:
            return user.get('movie_list', [])
        else:
            return None
        
    @staticmethod
    def remove_midia_from_list(user_id, midia_id):
        try:
            users_collection = db.users
            result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$pull": {"midia_list": midia_id}})
            return result.modified_count > 0
        except Exception as e:
            print(f"Error deleting midia details from user: {e}")
            return False

    @staticmethod
    def remove_midia_from_watched_movies(user_id, midia_id):
        try:
            users_collection = db.users
            result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$pull": {"watched_midias": midia_id}})
            return result.modified_count > 0
        except Exception as e:
            print(f"Error removing movie from watched media of user: {e}")
            return False
        
 
  
        
    
    
    