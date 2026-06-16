import os

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
