from flask import Flask
from flask_pymongo import pymongo
from app import app

CONNECTION_STRING = "mongodb+srv://safetakeoff:safetakeoff@sto.8o3avqd.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('safetakeoff')
user_collection = pymongo.collection.Collection(db, 'test')


