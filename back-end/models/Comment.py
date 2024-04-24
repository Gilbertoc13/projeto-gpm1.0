from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.Media import MediaAPI
from pymongo import MongoClient
from bson import ObjectId, json_util
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))
api_key = os.getenv('TMDB_KEY')


import requests

class Comment:
    @staticmethod
    def get_media_details(tmdb_id, media_type, api_key):
        base_url = "https://api.themoviedb.org/3/"
        url = f"{base_url}{media_type}/{tmdb_id}?api_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data:", response.text)
            return None

    @staticmethod
    @jwt_required()
    def create_comment(tmdb_id, media_type, review,is_spoiler, stars):
        try:
            user_id = get_jwt_identity()
            media_details = Comment.get_media_details(tmdb_id, media_type, api_key)
        
            if media_details:
                media_id = media_details.get("id")
                media_title = media_details.get("title") if media_type == "movie" else media_details.get("name")
                

                new_comment = {
                    "user_id": ObjectId(user_id),
                    "media_id": media_id,
                    "media_type": media_type,
                    "media_title": media_title,
                    "review": review,
                    "stars": stars,
                    "is_spoiler":  is_spoiler
                }

                comment_id = db.comments.insert_one(new_comment).inserted_id
                
                MediaAPI.add_comment_to_media(tmdb_id, comment_id, review, user_id, media_type, media_title, is_spoiler, stars)
                return str(comment_id)  
               
            else:
                print("Media details not found")
                return None
        except Exception as e:
            print(f"Error creating comment: {e}")
            return None


    @staticmethod
    def get_comments_by_user():
     try:
        user_id = get_jwt_identity()
        comments_collection = db.comments
        comments = comments_collection.find({"user_id": ObjectId(user_id)})
        comments = [json.loads(json_util.dumps(comment)) for comment in comments]
        return jsonify({"comments": comments}), 200
     except Exception as e:
        print(f"Error retrieving comments by user: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    @staticmethod
    @jwt_required()
    def get_comments_by_media_id_route(tmdb_id, media_type):
     try:
        comments_collection = db.comments
        tmdb_id_str = str(tmdb_id)
        comments = comments_collection.find({"media_id": tmdb_id_str, "media_type": media_type})

        comments = [json.loads(json_util.dumps(comment)) for comment in comments]

        return jsonify({"comments": comments}), 200
     except Exception as e:
        print(f"Error retrieving comments for media {tmdb_id}: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
     
    


    @staticmethod
    @jwt_required()
    def update_comment(comment_id, review, is_spoiler, stars):
        try:
            user_id = get_jwt_identity()
            comments_collection = db.comments
            update_result = comments_collection.update_one(
                {'_id': ObjectId(comment_id), 'UserId': ObjectId(user_id)},
                {'$set': {'review': review, 'is_spoiler': is_spoiler, 'stars': stars}}
            )
            if update_result.matched_count == 1:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error updating comment: {e}")
            return None

    @staticmethod
    @jwt_required()
    def delete_comment(comment_id):
        try:
            user_id = get_jwt_identity()
            comments_collection = db.comments
            delete_result = comments_collection.delete_one({'_id': ObjectId(comment_id), 'UserId': ObjectId(user_id)})
            if delete_result.deleted_count == 1:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error deleting comment: {e}")
            return None
