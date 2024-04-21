
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from pymongo import MongoClient
from bson import ObjectId,json_util
import os
from dotenv import load_dotenv


load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))
api_key= os.getenv('TMDB_KEY')


class Comment:
    @staticmethod
    @jwt_required() 
    def create_comment(tmdb_id, comment, is_spoiler):
        try:
            user_id = get_jwt_identity() 
            comments_collection = db.comments
            new_comment = {
                "user_id": user_id,
                "tmdb_id": tmdb_id,
                "comment": comment,
                "is_spoiler": is_spoiler
            }

            result = comments_collection.insert_one(new_comment)
            return str(result.inserted_id)

        except Exception as e:
            print(f"Error creating comment: {e}")
            return None
   
    @staticmethod
    @jwt_required()  
    def get_comments_by_user_route():
      try:
        user_id = get_jwt_identity()  
        comments_collection = db.comments
        comments = comments_collection.find({"user_id": user_id})

        
        comments = [json_util.dumps(comment) for comment in comments]

        return jsonify({"comments": comments}), 200
      except Exception as e:
        print(f"Error retrieving comments: {e}")
        return jsonify({"message": "Failed to retrieve comments"}), 500
   
    @staticmethod
    @jwt_required()  
    def update_comment(comment_id, comment, is_spoiler):
        try:
            user_id = get_jwt_identity()  
            comments_collection = db.comments

            update_result = comments_collection.update_one(
                {'_id': ObjectId(comment_id), 'user_id': user_id},  
                {'$set': {'comment': comment, 'is_spoiler': is_spoiler}}
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

            delete_result = comments_collection.delete_one({'_id': ObjectId(comment_id), 'user_id': user_id})  

            if delete_result.deleted_count == 1:
                return True  
            else:
                return False 

        except Exception as e:
            print(f"Error deleting comment: {e}")
            return None






