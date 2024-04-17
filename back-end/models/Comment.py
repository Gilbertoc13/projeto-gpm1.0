
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))

class Comment:
    @staticmethod
    def create_comment_evaluation_model(username, user_id, content, is_spoiler, media_id):
        try:
            comments_collection = db.comments
            new_evaluation = {
                "midia_id": media_id,
                "user_id": user_id,
                "username": username,
                "content": content,
                "is_spoiler": is_spoiler
            }
            result = comments_collection.insert_one(new_evaluation)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating comment: {e}")
            return None

    @staticmethod
    def update_comment(comment_id, updated_fields):
        try:
            comments_collection = db.comments
            result = comments_collection.update_one({"_id": ObjectId(comment_id)}, {"$set": updated_fields})
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating comment: {e}")
            return False

    @staticmethod
    def delete_comment(comment_id):
        try:
            comments_collection = db.comments
            result = comments_collection.delete_one({"_id": ObjectId(comment_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting comment: {e}")
            return False

    @staticmethod
    def get_comment_by_id(comment_id):
        try:
            comments_collection = db.comments
            comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
            return comment
        except Exception as e:
            print(f"Error retrieving comment: {e}")
            return None






