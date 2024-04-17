
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))

class Comment:
    @staticmethod
    def create_comment(user_id, tmdb_id, is_spoiler):
        try:
            comments_collection = db.comments
            new_comment = {
                "user_id": user_id,
                "tmdb_id": tmdb_id,  
                "comment": [],
                "is_spoiler": is_spoiler
            }

            result = comments_collection.insert_one(new_comment)
            return str(result.inserted_id)

        except Exception as e:
            print(f"Error creating comment: {e}")
            return None
   
    @staticmethod
    def get_comments_by_user(user_id):
        try:
            comments_collection = db.comments
            return comments_collection.find({"user_id": user_id})

        except Exception as e:
            print(f"Error retrieving comments: {e}")
            return None
   
    @staticmethod
    def update_comment(comment_id, comment, is_spoiler):
        try:
            comments_collection = db.comments

            update_result = comments_collection.update_one(
                {'_id': ObjectId(comment_id)},
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
    def delete_comment(comment_id):
        try:
            comments_collection = db.comments

            delete_result = comments_collection.delete_one({'_id': ObjectId(comment_id)})

            if delete_result.deleted_count == 1:
                return True  
            else:
                return False 

        except Exception as e:
            print(f"Error deleting comment: {e}")
            return None






