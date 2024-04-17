
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
        try:
            midia_collection = db.midiq
            new_midia = {
                "title": title,
                "type": movie_type,
                "image_url": image_url,
                "comments": []
            }

            result = midia_collection.insert_one(new_midia)
            return str(result.inserted_id)

        except Exception as e:
            print(f"Error creating media: {e}")
            return None

    @staticmethod
    def get_midia_by_id(media_id):
        try:
            midia_collection = db.midia
            return midia_collection.find_one({'_id': ObjectId(media_id)})

        except Exception as e:
            print(f"Error retrieving media: {e}")
            return None

    @staticmethod
    def update_midia(media_id, title=None, image_url=None, movie_type=None):
        try:
            midia_collection = db.midia

         
            update_document = {}
            if title:
                update_document['title'] = title
            if image_url:
                update_document['image_url'] = image_url
            if movie_type:
                update_document['type'] = movie_type

            if update_document:  
                update_result = midia_collection.update_one(
                    {'_id': ObjectId(media_id)},
                    {'$set': update_document}
                )

                if update_result.matched_count == 1:
                    return True  
                else:
                    return False  

            else:
                return False 

        except Exception as e:
            print(f"Error updating media: {e}")
            return None

    @staticmethod
    def delete_midia(media_id):
        try:
            midia_collection = db.midia

            delete_result = midia_collection.delete_one({'_id': ObjectId(media_id)})

            if delete_result.deleted_count == 1:
                return True  
            else:
                return False  

        except Exception as e:
            print(f"Error deleting media: {e}")
            return None
    
    @staticmethod
    def get_media_comments(media_id):
        try:
            midia_collection = db.midia

            
            media_data = midia_collection.find_one({'_id': ObjectId(media_id)})

            if media_data:
                
                comments = media_data['comments']
                return comments
            else:
                return None

        except Exception as e:
            print(f"Error retrieving media comments: {e}")
            return None

 
    
  
