from pymongo import MongoClient
from datetime import datetime, UTC
from contextlib import contextmanager
from local_settings1 import MONGODB_URL_WRITE, MONGODB_DB_NAME, MONGODB_COLLECTION_NAME

@contextmanager
def get_mongodb_collection():
    """
    Creates and manages a connection to a MongoDB collection.
    """
    client = None
    try:
        client = MongoClient(MONGODB_URL_WRITE)
        db = client[MONGODB_DB_NAME]
        collection = db[MONGODB_COLLECTION_NAME]
        yield collection
    except Exception as e:
        print(f"Error connecting to MySQL: {e}❌")
        yield None
    finally:
        if client:
            client.close()

def log_search_query(search_type, params, results_count):
    """
    Writes a search query to MongoDB.
    """
    with get_mongodb_collection() as collection:
        if collection is None:
            return
        log_entry = {
            "timestamp": datetime.now(UTC),
            "search_type": search_type,
            "params": params,
            "results_count": results_count
        }
        try:
            collection.insert_one(log_entry)
        except Exception as e:
            print(f"Error when writing log to MongoDB: {e}❌")
