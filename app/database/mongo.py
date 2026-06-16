from pymongo import MongoClient

def get_client(uri: str = None):
    """Return a MongoClient connected to the given URI or localhost."""
    return MongoClient(uri or "mongodb://localhost:27017")
