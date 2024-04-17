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
    def add_movie_to_watchlist(user_id, movie_id):
        try:
            users_collection = db.users

            existing_watchlist = users_collection.find_one({'_id': ObjectId(user_id)}, {'watchlist': 1})
            if existing_watchlist and 'watchlist' in existing_watchlist:
                if movie_id in existing_watchlist['watchlist']:
                    return {'message': 'Movie already exists in watchlist'}, 400

            
            update_result = users_collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$push': {'watchlist': movie_id}}
            )

            if update_result.modified_count == 1:
                return {'message': 'Movie added to watchlist successfully'}, 200
            else:
                return {'message': 'Error adding movie to watchlist'}, 500

        except Exception as e:
            print(f"Error adding movie to watchlist: {e}")
            return {'message': 'Internal server error'}, 500

    @staticmethod
    def delete_movie_from_watchlist(user_id, movie_id):
        try:
            users_collection = db.users

            update_result = users_collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$pull': {'watchlist': movie_id}}
            )

            if update_result.modified_count == 1:
                return {'message': 'Movie removed from watchlist successfully'}, 200
            elif update_result.matched_count == 0:
                return {'message': 'User not found'}, 404
            else:
                return {'message': 'Error removing movie from watchlist'}, 500

        except Exception as e:
            print(f"Error removing movie from watchlist: {e}")
            return {'message': 'Internal server error'}, 500
 
  
        
    
    
    