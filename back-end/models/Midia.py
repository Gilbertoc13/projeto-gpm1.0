
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv


load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))

class Midia:
    @staticmethod
    def create_midia(title, image_url, movie_type):
      midia_collection = db.midia
      new_midia = {
        "title": title,
        "type": movie_type,  
        "image_url": image_url,
        "comments": []
    }
      result = midia_collection.insert_one(new_midia)
      return {
        "title": title,
        "id": str(result.inserted_id),  
        "type": movie_type,
        "comment": []
    }

    @staticmethod
    def get_all_midia_ids():
        midia_collection = db.midia
        midia_ids = [movie['_id'] for movie in midia_collection.find()] 
        return midia_ids


    @staticmethod
    def get_midia_by_title(title, movie_type):
        midia_collection = db.midia
        midia = midia_collection.find_one({"title": title, "type": movie_type})
        return midia

    @staticmethod
    def get_midia_by_id_model(midia_id, movie_type="movie"):
      midia_collection = db.midia
      midia = midia_collection.find_one(
        {"_id": midia_id, "type": movie_type}, projection={"title": 1, "image_url": 1}
    )
      return midia

    @staticmethod
    def update_midia(midia_id, updated_fields):
        midia_collection = db.midia
        result = midia_collection.update_many({"_id": ObjectId(midia_id)}, {"$set": updated_fields})
        return result

    @staticmethod
    def delete_midia(midia_id):
        midia_collection = db.midia
        result = midia_collection.find_one_and_delete({"_id": ObjectId(midia_id)})
        return result
    
    @staticmethod
    def get_comments(midia_id, content=None):
      midia_collection = db.midia
      query = {"_id": ObjectId(midia_id)}

      if content is not None:
        query["comments.content"] = content

      midia = midia_collection.find_one(query)
    
      if midia:
        return midia.get('comments', [])
      else:
        return []

    
    
    

 
    
  
