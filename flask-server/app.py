from flask import Flask, render_template, request, url_for, redirect
from flask import jsonify
import json
from flask.json import JSONEncoder
import pandas as pd

from bson import json_util, ObjectId# from db import get_db
from datetime import datetime
import json
from flask_cors import CORS,cross_origin
from flask_restful import Api




# from werkzeug.local import LocalProxy


import db
#test to insert data to the data base

# db = LocalProxy(get_db)
class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)

app = Flask(__name__)
CORS(app)



app.json_encoder = MongoJsonEncoder



@app.route('/')
def flask_mongodb_atlas():
    return redirect('http://127.0.0.1:5173/')

# @app.route("/test",methods=['GET'])
# # @cross_origin(origin='*',headers=['Content- Type','Authorization'])

# def test():

    # d = db.user_collection.find({})
    # # dict.pop('_id')
    # df = pd.json_normalize(d)
    # dftempyear = pd.DataFrame(df.groupby(['year'])['temperature'].mean())
    
    # dftempyear['year'] = dftempyear.index

    
    # x= dftempyear['year'].to_list()
    # y=dftempyear['temperature'].to_list()
    # result={}
    # result['year']=x
    # result['temp']=y

    # # tempyear= dftempyear.to_json(orient='records')[1:-1].replace('},{', '} {')
    # # json_list = json.loads(json.dumps(list(dftempyear.T.to_dict().values())))
    
    # # return jsonify(list(d)[0])
    # return jsonify(result)

@app.route("/barchart",methods=['GET'])
# @cross_origin(origin='*',headers=['Content- Type','Authorization'])

def barchart():

    d = db.minmaxdata.find({})
    df = pd.json_normalize(d)
    df = df.sort_values('monthdate')

    result={}

    result['date']= df['monthdate'].to_list()
    result['temp']= df['temperature'].to_list()  
    result['wind']= df['wind_speed'].to_list()   
    result['press']= df['mean_sea_level_pressure'].to_list()   
    result['cloud']= df['total_cloud_cover'].to_list()   
    result['mintemp']= df['mintemp'].to_list()   
    result['minwind']= df['minwind'].to_list()   
    result['minpress']= df['minpress'].to_list()   
    result['mincloud']= df['mincloud'].to_list()   
    result['maxtemp']= df['maxtemp'].to_list()   
    result['maxwind']= df['maxwind'].to_list()   
    result['maxpress']= df['maxpress'].to_list()   
    result['maxcloud']= df['maxcloud'].to_list()  

    return jsonify(result) 


@app.route("/test",methods=['GET'])
# @cross_origin(origin='*',headers=['Content- Type','Authorization'])

def test():

    d = db.user_collection.find({})
    # dict.pop('_id')
    df = pd.json_normalize(d)
    dftempyear = pd.DataFrame(df.groupby(['year'])['temperature'].mean())
    
    dftempyear['year'] = dftempyear.index

    
    x= dftempyear['year'].to_list()
    y=dftempyear['temperature'].to_list()
    result={}
    result['year']=x
    result['temp']=y

    # tempyear= dftempyear.to_json(orient='records')[1:-1].replace('},{', '} {')
    # json_list = json.loads(json.dumps(list(dftempyear.T.to_dict().values())))
    
    # return jsonify(list(d)[0])
    return jsonify(result)

@app.route("/yearlyavg",methods=['GET'])
# @cross_origin(origin='*',headers=['Content- Type','Authorization'])

def yearlyavg():

    d = db.yearlyavg.find({})
    df = pd.json_normalize(d)
    df = df.sort_values('year')

    result={}

    result['year']= df['year'].to_list()
    result['temp']= df['temperature'].to_list()  
    result['wind']= df['wind_speed'].to_list()   
    result['press']= df['mean_sea_level_pressure'].to_list()   
    result['cloud']= df['total_cloud_cover'].to_list()   
   
    return jsonify(result)  



    
@app.route("/monthlyavg",methods=['GET'])
# @cross_origin(origin='*',headers=['Content- Type','Authorization'])

def monthlyavg():

    d = db.monthlyavg.find({})
    df = pd.json_normalize(d)
    df = df.sort_values('month')

    result={}

    result['month']= df['month'].to_list()
    result['temp']= df['temperature'].to_list()  
    result['wind']= df['wind_speed'].to_list()   
    result['press']= df['mean_sea_level_pressure'].to_list()   
    result['cloud']= df['total_cloud_cover'].to_list()   
   
    return jsonify(result)  

@app.route("/aircraftsdata",methods=['GET'])
def aircraftsdata():

    d = db.AirCrafts.find({})
    df = pd.json_normalize(d)
    # df = df.sort_values('Model')

    result={}

    result['Model']= df['Model'].to_list()
    # result['Make']= df['Make'].to_list()  
    result['Year']= df['Year'].to_list()   
    # result['Category']= df['Category'].to_list()   
    result['Temperature_t']= df['Temperature Threshold'].to_list()   
    result['Wind_t']= df['Wind Speed Threshold'].to_list()   
    # result['Solar_t']= df['Solar Radiation Threshold'].to_list()   
    result['Cloud_t']= df['Total Cloud Cover Threshold'].to_list()  
    result['humidity_t']= df['Relative Humidity Threshold'].to_list()   
    # result['thermal_t']= df['Thermal Radiation Threshold'].to_list()    

    return jsonify(result)  


@app.route("/aircraftspie",methods=['GET'])
def aircraftspie():

    d = db.AirCrafts.find({})
    df = pd.json_normalize(d)
    result={}

   
    Categories = df.groupby("Category")
    CategoryCount = df.groupby("Category")["Model"].count()
    Make = df.groupby("Make")
    MakeCount = df.groupby("Make")["Model"].count()

    result['Model']= df['Model'].to_list()
    result['Make']= list(Make.groups.keys())
    result['MakeCount']= MakeCount.to_list()  
    result['Categories'] = list(Categories.groups.keys())
    result['CategoryCount']= CategoryCount.to_list()   

    return jsonify(result)  

@app.route("/aircraftscategories",methods=['GET'])
def aircraftscategories():

    d = db.AirCrafts.find({})
    df = pd.json_normalize(d)
    result={}

    Categories = df.groupby("Category")
    result['Categories'] = list(Categories.groups.keys())

    return jsonify(result)  

@app.route("/temppred",methods=['GET'])

def temppred():
    d = db.TempPred.find({})
    df = pd.json_normalize(d)
    df = df.sort_values('ds')
    result={}
    result['ds']= df['ds'].to_list()
    result['yhat1']= df['yhat1'].to_list()  
   
    return jsonify(result)  


@app.route("/pressurepred",methods=['GET'])
def pressurepred():
    d = db.PressurePred.find({})
    df = pd.json_normalize(d)
    df = df.sort_values('ds')

    result={}
    result['ds']= df['ds'].to_list()
    result['yhat1']= df['yhat1'].to_list()  
   
    return jsonify(result) 

@app.route("/cloudpred",methods=['GET'])
def cloudpred():
    d = db.CloudCoverPred.find({})
    df = pd.json_normalize(d)
    df = df.sort_values('ds')

    result={}
    result['ds']= df['ds'].to_list()
    result['yhat1']= df['yhat1'].to_list()  
   
    return jsonify(result) 

@app.route("/windpred",methods=['GET'])
def windpred():
    d = db.WindspeedPred.find({})
    df = pd.json_normalize(d)
    df = df.sort_values('ds')

    result={}
    result['ds']= df['ds'].to_list()
    result['yhat1']= df['yhat1'].to_list()  
   
    return jsonify(result) 

if __name__ == '__main__':
    app.run(port=5000,debug=True)

