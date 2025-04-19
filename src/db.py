import os, logging
from pymongo import MongoClient
from bson import ObjectId
logging.basicConfig(level=logging.ERROR)
# for db store only python base variable

connection_uri = os.getenv("MONGO_URI", "")

class DB:
    def __init__(self):
        return
        try:
            client = MongoClient(connection_uri)
            db = client['Gardraw']
            self.collection = db['gameState']

            print("Connected to mongoDB")
            print("Database available: ", client.list_database_names())
        except Exception as e:
            logging.error("Failed to connected to mongoDB: ", e)

    def insert_to(self, obj, retries=3):
        return
        for attempt in range(retries):
            try:
                obj_dict = obj.to_dict()
                obj_dict.pop('_id', None)
                insert_result = self.collection.insert_one(obj_dict)
                _id = insert_result.inserted_id
                print("Inserted obj with ID: ", _id)
                obj._id = _id
                print("Insert id into obj._id")
                return
            except Exception as e:
                logging.error("Failed to insert to mongoDB: ", e)
    
    def update_to(self, obj, retries=3):
        return
        for attempt in range(retries):
            try:
                update_query = {"_id": obj._id}
                obj_dict = obj.to_dict()
                new_value = {"$set": obj_dict}
                self.collection.update_one(update_query, new_value)
                print("Object update successfuly")
                return
            except Exception as e:
                logging.error("Failed to update :", e)

    def delete_to(self, obj, retries=3):
        return
        for attempt in range(retries):
            try:
                _id = obj._id
                query = {"_id": ObjectId(_id)}
                delete_result = self.collection.delete_one(query)
                if delete_result.deleted_count > 0:
                    print(f"Successfully deleted object with ID: {_id}")
                    obj._id = None
                    return True  # Successfully deleted
                else:
                    raise Exception(f"No document found with _id: {_id}")
            except Exception as e:
                if attempt < retries - 1:
                    print(f"Retrying delete (attempt {attempt + 1})...")
                else:
                    print(f"Failed to delete after {retries} attempts: {e}")
                    return False  # Deletion failed


    def sync_from_db(self, obj):
        return
        try:
            obj_dict = obj.to_dict()
            data = self.collection.find_one({"_id": obj._id})
            if data:
                for key, value in data.item():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                print("Object Synchronized!")
        except Exception as e:
            logging.ERROR("Failed to synchronized:", e)



