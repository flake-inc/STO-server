from flask import Flask, render_template, request, url_for, redirect
from flask import jsonify
from flask import session
import config
import json
from flask.json import JSONEncoder
import pandas as pd
import os
from werkzeug.utils import secure_filename
import logging


from bson import json_util, ObjectId  # from db import get_db
from datetime import datetime
import json
from flask_cors import CORS, cross_origin
from flask_restful import Api
from flask_session import Session
import redis
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, jwt_required





# from werkzeug.local import LocalProxy


import db


UPLOAD_FOLDER = 'datasets'
ALLOWED_EXTENSIONS = set(['csv'])
# test to insert data to the data base
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('HELLO WORLD')


# db = LocalProxy(get_db)
class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


app = Flask(__name__)
# app.config.from_object(ApplicationConfig)

CORS(app, supports_credentials=True)


server_session = Session(app)
# app.config["secret_key"] = 'super secret key'
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_PERMANENT'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_SECRET_KEY"] = "safetakeoff"
jwt = JWTManager(app)
app.secret_key = "safetakeoff"




app.json_encoder = MongoJsonEncoder


@app.route('/upload', methods=['POST'])
@jwt_required()


def fileUpload():

    print(" dude")
    
    target=UPLOAD_FOLDER
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
    file = request.files["file"]
   
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)

    df = pd.read_csv("datasets/"+filename)
    response="File uploaded successfully"

    if filename=="monthlyavg.csv":
        x = json.loads(json.dumps(list(df.T.to_dict().values())))
        db.monthlyavg.insert_many(x)

    elif filename=="yearlyavg.csv":
        x = json.loads(json.dumps(list(df.T.to_dict().values())))
        db.monthlyavg.insert_many(x)

    elif filename=="weatherdatanew.csv":
        x = json.loads(json.dumps(list(df.T.to_dict().values())))
        db.user_collection.insert_many(x)


    elif filename=="allpred.csv":
        x = json.loads(json.dumps(list(df.T.to_dict().values())))
        db.allpred.insert_many(x)

    elif filename=="aircrafts.csv":
        x = json.loads(json.dumps(list(df.T.to_dict().values())))
        db.AirCrafts.insert_many(x)

    elif filename=="cloudcoverpred.csv":
        x = json.loads(json.dumps(list(df.T.to_dict().values())))
        db.CloudCoverPred.insert_many(x)

    elif filename=="temperaturepred.csv":
        x = json.loads(json.dumps(list(df.T.to_dict().values())))
        db.TempPred.insert_many(x)

    elif filename=="windspeedpred.csv":
        x = json.loads(json.dumps(list(df.T.to_dict().values())))
        db.WindSpeedPred.insert_many(x)

    elif filename=="pressurepred.csv":
        x = json.loads(json.dumps(list(df.T.to_dict().values())))
        db.PressurePred.insert_many(x)

    elif filename=="minmaxmean.csv":
        x = json.loads(json.dumps(list(df.T.to_dict().values())))
        db.minmaxdata.insert_many(x)

    elif filename=="test.csv":
        x = json.loads(json.dumps(list(df.T.to_dict().values())))
        db.test.insert_many(x)

   
         

    else:
        os.remove("datasets/"+filename)
        response = "Incorrect File name"
        return NameError
        # print("file not found")

    

    




    # session['uploadFilePath']=destination
   
    return jsonify(message=response)





@app.route("/login", methods=["POST"])
def User_Login():

    email = request.json['email']
    password = request.json["password"]
    print("hello", password)
    # Retrieve a user by email:
    user = db.user.find_one({'username': email})

    # if user is already register show this error message

    if user is None:
        return jsonify({'error': 'User error'}), 401

    if user['password'] != password:
        return jsonify({'error': 'Password error'}), 401

    # session["user_id"] = user['username']
    # print(session['user_id'])
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token, msg="you are Successfully Logged In")




@jwt_required()

@app.route("/addstaff", methods=["GET","POST"])
def addstaff():
    print('hi')
    # current_user = get_jwt_identity()

    email = request.json.get('email',None)
    password = request.json["password"]
    print("hello", password)
    # Retrieve a user by email:
    user = db.user.find_one({'username': email})
    print(user)
    # if user is already register show this error message

    if user  is not None:
        return jsonify({'error': 'User already exists'}), 401

    # if user['password'] != password:
    #     return jsonify({'error': 'Password error'}), 401

    # session["user_id"] = user['username']
    # print(session['user_id'])
    # access_token = create_access_token(identity=email)
    # return jsonify(access_token=access_token, msg="you are Successfully Logged In")
    db.user.insert_one({'username':email,'password':password})

    return jsonify({'message': 'Staff added successfully'})


# @app.route("/logout", methods=["POST"])
# def User_Logout():
#     print(session)
#     session.pop(session["user_id"])
#     return "200"



@jwt_required()

@app.route("/isloggedin", methods=["GET"])
def isloggedin():
 

    return jsonify({'message': 'Logged in'})


# @app.route("/logout", methods=["POST"])
# def User_Logout():
#     print(session)
#     session.pop(session["user_id"])
#     return "200"



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


@app.route("/barchart", methods=['GET'])
# @cross_origin(origin='*',headers=['Content- Type','Authorization'])
def barchart():

    d = db.minmaxdata.find({})
    df = pd.json_normalize(d)
    df = df.sort_values('monthdate')

    result = {}

    result['date'] = df['monthdate'].to_list()
    result['temp'] = df['temperature'].to_list()
    result['wind'] = df['wind_speed'].to_list()
    result['press'] = df['mean_sea_level_pressure'].to_list()
    result['cloud'] = df['total_cloud_cover'].to_list()
    result['mintemp'] = df['mintemp'].to_list()
    result['minwind'] = df['minwind'].to_list()
    result['minpress'] = df['minpress'].to_list()
    result['mincloud'] = df['mincloud'].to_list()
    result['maxtemp'] = df['maxtemp'].to_list()
    result['maxwind'] = df['maxwind'].to_list()
    result['maxpress'] = df['maxpress'].to_list()
    result['maxcloud'] = df['maxcloud'].to_list()

    return jsonify(result)






@app.route("/getpred", methods=['GET'])
@jwt_required()


def getpred():

    user_id = get_jwt_identity()
    print(user_id)

    today = datetime.today().strftime('%Y-%m-%d')

    d = db.allpred.find({'date': today})
    df = pd.json_normalize(d)
    df = df.drop(['_id'], axis=1)
    df = df.sort_values('hour')
    # df =json.loads(json.dumps(list(df.T.to_dict().values())))

    # result={}

    # result['temp']= df['temperature'].to_list()
    # result['date']= df['datestamp'].to_list()
    # result['hour']= df['hour'].to_list()
    # result['wind']= df['windspeed'].to_list()
    # result['press']= df['pressure'].to_list()
    # result['cloud']= df['cloudcover'].to_list()

    json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
    return jsonify(json_list)


@app.route("/test", methods=['GET'])
def test():

    df = pd.read_csv('submission8.csv')
    x = json.loads(json.dumps(list(df.T.to_dict().values())))

    db.test.insert_many(x)

    return x

# @app.route("/login",methods=['GET'])

# def login():
#     d = db.user.find({})
#     df = pd.json_normalize(d)
#     df = df.sort_values('monthdate')
#     df = pd.read_csv('submission8.csv')
#     x = json.loads(json.dumps(list(df.T.to_dict().values())))

#     db.test.insert_many(x)

#     return x


@app.route("/yearlyavg", methods=['GET'])
def yearlyavg():

    d = db.yearlyavg.find({})
    df = pd.json_normalize(d)
    df = df.sort_values('year')

    result = {}

    result['year'] = df['year'].to_list()
    result['temp'] = df['temperature'].to_list()
    result['wind'] = df['wind_speed'].to_list()
    result['press'] = df['mean_sea_level_pressure'].to_list()
    result['cloud'] = df['total_cloud_cover'].to_list()

    return jsonify(result)


@app.route("/monthlyavg", methods=['GET'])
def monthlyavg():

    d = db.monthlyavg.find({})
    df = pd.json_normalize(d)
    df = df.sort_values('month')

    result = {}

    result['month'] = df['month'].to_list()
    result['temp'] = df['temperature'].to_list()
    result['wind'] = df['wind_speed'].to_list()
    result['press'] = df['mean_sea_level_pressure'].to_list()
    result['cloud'] = df['total_cloud_cover'].to_list()

    return jsonify(result)


@app.route("/aircraftsdata", methods=['GET'])
def aircraftsdata():

    d = db.AirCrafts.find({})
    df = pd.json_normalize(d)

    result = {}
    result['Model'] = df['Model'].to_list()
    result['Temperature_t'] = df['Temperature Threshold'].to_list()
    result['Wind_t'] = df['Wind Speed Threshold'].to_list()
    result['Cloud_t'] = df['Total Cloud Cover Threshold'].to_list()

    return jsonify(result)


@app.route("/aircraftspie", methods=['GET'])
def aircraftspie():

    cat = db.AirCrafts.aggregate([
        {"$group": {"_id": "$Category", "count": {"$sum": 1}}}
    ])

    make = db.AirCrafts.aggregate([
        {"$group": {"_id": "$Make", "count": {"$sum": 1}}}
    ])

    cat_arr = []
    cat_count_arr = []
    make_arr = []
    make_count_arr = []

    for i in cat:
        cat_arr.append(i['_id'])
        cat_count_arr.append(i["count"])

    for i in make:
        make_arr.append(i['_id'])
        make_count_arr.append(i["count"])

    result={}
    result['Make']= make_arr
    result['MakeCount']= make_count_arr
    result['Categories'] = cat_arr
    result['CategoryCount']= cat_count_arr
    return jsonify(result)


@app.route("/aircraftscategories", methods=['GET'])
def aircraftscategories():

    d = db.AirCrafts.distinct("Category")
    result = {}
    result['Categories'] = d

    return jsonify(result)


@app.route("/temppred", methods=['GET'])
def temppred():
    d = db.TempPred.find().limit(6000)
    df = pd.json_normalize(d)
    df = df.sort_values('ds')
    result = {}

    result['ds'] = df['ds'].to_list()
    result['yhat1'] = df['yhat1'].to_list()

    return jsonify(result)


@app.route("/pressurepred", methods=['GET'])
def pressurepred():
    d = db.PressurePred.find().limit(6000)
    df = pd.json_normalize(d)
    df = df.sort_values('ds')

    result = {}
    result['ds'] = df['ds'].to_list()
    result['yhat1'] = df['yhat1'].to_list()

    return jsonify(result)


@app.route("/cloudpred", methods=['GET'])
def cloudpred():
    d = db.CloudCoverPred.find().limit(6000)
    df = pd.json_normalize(d)
    df = df.sort_values('ds')

    result = {}
    result['ds'] = df['ds'].to_list()
    result['yhat1'] = df['yhat1'].to_list()

    return jsonify(result)


@app.route("/windpred", methods=['GET'])
def windpred():
    d = db.WindSpeedPred.find().limit(6000)
    df = pd.json_normalize(d)
    df = df.sort_values('ds')

    result = {}
    result['ds'] = df['ds'].to_list()
    result['yhat1'] = df['yhat1'].to_list()

    return jsonify(result)


@app.route("/check_today_danger", methods=['GET'])
def check_today_danger():
    dangered_aircrafts = []
    model_list = []
    make_list = []
    cat_list = []
    year_list = []
    REG_list = []

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    new_dt = dt_string[:13] + ":00:00"
    print("\n====================================")
    print("local time:", new_dt)

    wind = db.WindSpeedPred.find_one({"ds": new_dt})
    print("wind predict", wind['yhat1'])

    temp = db.TempPred.find_one({"ds": new_dt})
    print("temp predict", temp['yhat1'])

    cloud = db.CloudCoverPred.find_one({"ds": new_dt})
    print("cloud cover predict", cloud['yhat1'])

    aircrafts = db.AirCrafts.find({})
    df_air = pd.json_normalize(aircrafts)

    for i in df_air.index:
        if float(df_air['Wind Speed Threshold'][i]) <= float(wind['yhat1']):
            dangered_aircrafts.append(df_air['_id'][i])
            model_list.append(df_air['Model'][i])
            make_list.append(df_air['Make'][i])
            cat_list.append(df_air['Category'][i])
            year_list.append(df_air['Year'][i])
            REG_list.append(df_air['REG'][i])
            continue

        if float(df_air['Temperature Threshold'][i]) <= float(temp['yhat1']):
            dangered_aircrafts.append(df_air['_id'][i])
            model_list.append(df_air['Model'][i])
            make_list.append(df_air['Make'][i])
            cat_list.append(df_air['Category'][i])
            year_list.append(df_air['Year'][i])
            REG_list.append(df_air['REG'][i])
            continue

        if float(df_air['Total Cloud Cover Threshold'][i]) <= float(cloud['yhat1']):
            dangered_aircrafts.append(df_air['_id'][i])
            model_list.append(df_air['Model'][i])
            make_list.append(df_air['Make'][i])
            cat_list.append(df_air['Category'][i])
            year_list.append(df_air['Year'][i])
            REG_list.append(df_air['REG'][i])
            continue

    result = {}

    result['Model'] = model_list
    result['Make'] = make_list
    result['Category'] = cat_list
    result['Year'] = make_list
    result['REG'] = cat_list
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
