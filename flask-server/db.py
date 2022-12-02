from flask import Flask
from flask_pymongo import pymongo
from app import app

# import bson

# from flask import current_app, g
# from werkzeug.local import LocalProxy



# def get_db():
#     """
#     Configuration method to return db instance
#     """
#     db = getattr(g, "_database", None)
#     if db is None:
#         db = g._database = PyMongo(current_app).db

#     return db


CONNECTION_STRING = "mongodb+srv://safetakeoff:safetakeoff@sto.8o3avqd.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('safetakeoff')
print("\n\nDatabase Connected!")
print("=====================")

user_collection = pymongo.collection.Collection(db, 'weatherdatanew')
minmaxdata = pymongo.collection.Collection(db, 'minmaxmeandata')
yearlyavg = pymongo.collection.Collection(db, 'yearlyavg')
monthlyavg = pymongo.collection.Collection(db, 'monthlyavg')
AirCrafts = pymongo.collection.Collection(db, 'AirCrafts')
TempPred = pymongo.collection.Collection(db, 'TempPred')
CloudCoverPred = pymongo.collection.Collection(db, 'CloudCoverPred')
PressurePred = pymongo.collection.Collection(db, 'PressurePred')
WindSpeedPred = pymongo.collection.Collection(db, 'WindSpeedPred')
test = pymongo.collection.Collection(db, 'test')
user = pymongo.collection.Collection(db, 'user')
# temppred = pymongo.collection.Collection(db, 'TempPred')
# windpred = pymongo.collection.Collection(db, 'WindSpeedPred')
# cloudpred = pymongo.collection.Collection(db, 'CloudCoverPred')
# presspred = pymongo.collection.Collection(db, 'PressurePred')
allpred = pymongo.collection.Collection(db, 'AllPred')







