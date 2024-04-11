
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))

class comment:

    @staticmethod
    def create_comment_evaluation_model(comment_id, user_id, rating, timestamp):
      comments_collection = db.comments
      new_evaluation = {
        "comment_id": comment_id,
        "user_id": user_id,
        "rating": rating,
        "timestamp": timestamp,
    }
      result = comments_collection.insert_one(new_evaluation)
      return str(result.inserted_id)

    @staticmethod
    def get_comment_evaluations(comment_id):
      comments_collection = db.comments
      comment = comments_collection.find_one({"_id": comment_id}, {"_id": 0, "evaluations": 1})
      return comment.get("evaluations", []) if comment else []
    
    @staticmethod
    def delete_comment_evaluation(comment_id, user_id):
      comments_collection = db.comments
      evaluation = comments_collection.find_one(
        {"_id": comment_id, "evaluations.user_id": user_id}, {"_id": 0, "evaluations": 1}
    )
      if evaluation:
        comments_collection.update_one(
            {"_id": comment_id},
            {"$pull": {"evaluations": {"user_id": user_id}}},
        )
      else:
        raise ValueError(f"Avaliação não encontrada para o usuário {user_id} no comentário {comment_id}")
    
    @staticmethod
    def update_comment_evaluation(comment_id, user_id, new_rating):
      comments_collection = db.comments
      evaluation = comments_collection.find_one(
        {"_id": comment_id, "evaluations.user_id": user_id}, {"_id": 0, "evaluations": 1}
    )
      if evaluation:
        comments_collection.update_one(
            {"_id": comment_id, "evaluations.user_id": user_id},
            {"$set": {"evaluations.$.rating": new_rating}},
        )
      else:
        raise ValueError(f"Avaliação não encontrada para o usuário {user_id} no comentário {comment_id}")









