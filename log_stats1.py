from log_writer1 import get_mongodb_collection

def get_popular_queries():
    """
    Returns the 5 most frequent search queries.
    """
    with get_mongodb_collection() as collection:
        if collection is None:
            return []
        try:
            results = [
                {
                    "$group": {
                        "_id": {
                            "search_type": "$search_type",
                            "params": "$params"
                        },
                        "count": {"$sum": 1}
                    }
                },
                {"$sort": {"count": -1}},
                {"$limit": 5}
            ]
            return list(collection.aggregate(results))
        except Exception as e:
            print(f"Error receiving popular queries from MongoDB: {e}❌")
            return []

def get_recent_queries():
    """
    Returns the last 5 search queries.
    """
    with get_mongodb_collection() as collection:
        if collection is None:
            return []
        try:
            return list(collection.find().sort("timestamp", -1).limit(5))
        except Exception as e:
            print(f"Error receiving the latest requests from MongoDB: {e}❌")
            return []