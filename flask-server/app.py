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
from werkzeug.security import generate_password_hash, check_password_hash


# from werkzeug.local import LocalProxy


import db


UPLOAD_FOLDER = 'datasets'
ALLOWED_EXTENSIONS = set(['csv'])
# test to insert data to the data base
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Safe-TakeOff by flake inc.')

# db = LocalProxy(get_db)


class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


def server_init():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)  
    # app.config.from_object(ApplicationConfig)
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
    print("\nSafe-TakeOff by flake inc.")
    print("Backend Started!")
    print("=====================\n\n")


    @app.route('/upload', methods=['POST'])
    @jwt_required()
    def fileUpload():

        print(" dude")

        target = UPLOAD_FOLDER
        if not os.path.isdir(target):
            os.mkdir(target)
        logger.info("welcome to upload`")
        file = request.files["file"]

        filename = secure_filename(file.filename)
        destination = "/".join([target, filename])
        file.save(destination)

        df = pd.read_csv("datasets/"+filename)
        response = "File uploaded successfully"

        if filename == "monthlyavg.csv":
            x = json.loads(json.dumps(list(df.T.to_dict().values())))
            db.monthlyavg.insert_many(x)

        elif filename == "yearlyavg.csv":
            x = json.loads(json.dumps(list(df.T.to_dict().values())))
            db.monthlyavg.insert_many(x)

        elif filename == "weatherdatanew.csv":
            x = json.loads(json.dumps(list(df.T.to_dict().values())))
            db.user_collection.insert_many(x)

        elif filename == "allpred.csv":
            x = json.loads(json.dumps(list(df.T.to_dict().values())))
            db.allpred.insert_many(x)

        elif filename == "aircrafts.csv":
            x = json.loads(json.dumps(list(df.T.to_dict().values())))
            db.AirCrafts.insert_many(x)

        elif filename == "cloudcoverpred.csv":
            x = json.loads(json.dumps(list(df.T.to_dict().values())))
            db.CloudCoverPred.insert_many(x)

        elif filename == "temperaturepred.csv":
            x = json.loads(json.dumps(list(df.T.to_dict().values())))
            db.TempPred.insert_many(x)

        elif filename == "windspeedpred.csv":
            x = json.loads(json.dumps(list(df.T.to_dict().values())))
            db.WindSpeedPred.insert_many(x)

        elif filename == "pressurepred.csv":
            x = json.loads(json.dumps(list(df.T.to_dict().values())))
            db.PressurePred.insert_many(x)

        elif filename == "minmaxmean.csv":
            x = json.loads(json.dumps(list(df.T.to_dict().values())))
            db.minmaxdata.insert_many(x)

        elif filename == "test.csv":
            x = json.loads(json.dumps(list(df.T.to_dict().values())))
            db.test.insert_many(x)

        else:
            os.remove("datasets/"+filename)
            response = "Incorrect File name"
            return NameError
            # print("file not found")

        # session['uploadFilePath']=destination

        return jsonify(message=response)

    @jwt_required()

    @app.route('/prediction', methods=['POST'])
    def prediction():

        


        import pandas as pd
        import matplotlib.pyplot as plt
        from datetime import datetime, datetime, timedelta, date
        import seaborn as sns
        from neuralprophet import NeuralProphet
        import warnings
        warnings.filterwarnings('ignore')



        df = pd.read_csv("datasets/weather_data.csv")

        df['time_stamp'] = pd.to_datetime(df['time_stamp'])
        df.set_index('time_stamp')

        df.info()

        df.describe

        temp_smooth = df.temperature.rolling(window=24).mean()
        temp_smooth.isnull().sum()

        temp = df.drop('time_stamp', axis=1)



        df['date'] = df['time_stamp'].dt.date
        df['year'] = df['time_stamp'].dt.year
        df['month'] = df['time_stamp'].dt.month



        df2 = df[['temperature','dewpoint_temperature','wind_speed','mean_sea_level_pressure','relative_humidity','surface_solar_radiation','surface_thermal_radiation','total_cloud_cover']]

        print('Hello',1)

        from statsmodels.tsa.seasonal import seasonal_decompose

        temp_add_decomp = seasonal_decompose(df.temperature, model='multiplicative', extrapolate_trend='freq', period=365*24)



        df1 = df[df['date'] >= date(2017,1,1)]
        dfbefore2021 = df[df['year']<2021]


        print('Hello',2)


        df = pd.read_csv("datasets/weather_data.csv")[['time_stamp', 'temperature']]
        df.time_stamp = pd.to_datetime(df.time_stamp)

        avgtemp = pd.DataFrame(df1.groupby(['date'])['temperature'].mean())
        temp_add = seasonal_decompose(avgtemp['temperature'], model='additive',extrapolate_trend='freq',period=365)



        yearlytemp = pd.DataFrame(dfbefore2021.groupby(['year'])['temperature'].mean())

        print('Hello',3)

        df.rename(columns = {'time_stamp':'ds', 'temperature':'y'}, inplace = True)


        print('Hello',4)


        m = NeuralProphet(changepoints_range=0.95, 
                        n_changepoints=50, 
                        trend_reg=1, 
                        weekly_seasonality=False, 
                        daily_seasonality=10, 
                        yearly_seasonality=10)

        df['ds'] = pd.DatetimeIndex(df['ds'])
        df.head()

        df_train, df_val = m.split_df(df, freq='H', valid_p = 0.2)
        metrics = m.fit(df_train, freq='H', validation_df=df_val)

        seasonal_components = m.predict_seasonal_components(df)
        seasonal_components

        metrics



        future = m.make_future_dataframe(df, periods=24*365*2, n_historic_predictions=len(df))
        future.tail()

        forecast = m.predict(future)

        forecast

        forecast_df = forecast.copy()
        forecast_df.info()

        df.info()




        forecast.to_csv( "temperature_prediction.csv", index=False)
        print("hello")
        """# <a>Wind Speed</a>"""

        df = pd.read_csv("datasets/weather_data.csv")[['time_stamp', 'wind_speed']]

        df.time_stamp = pd.to_datetime(df.time_stamp)

        avgwindspeed = pd.DataFrame(df1.groupby(['date'])['wind_speed'].mean())
        windspeed_add = seasonal_decompose(avgwindspeed['wind_speed'], model='additive',extrapolate_trend='freq',period=365)



        monthlywind = pd.DataFrame(dfbefore2021.groupby(['month'])['wind_speed'].mean())
        months=['January','February','March','April','May','June','July','August','Sepetember','October','November','December']
        monthlywind['Month']=months


        df.rename(columns = {'time_stamp':'ds', 'wind_speed':'y'}, inplace = True)



        m = NeuralProphet(changepoints_range=0.95, 
                        n_changepoints=50, 
                        trend_reg=1, 
                        weekly_seasonality=False, 
                        daily_seasonality=10, 
                        yearly_seasonality=10)

        df['ds'] = pd.DatetimeIndex(df['ds'])
        df.head()

        m = NeuralProphet(changepoints_range=0.95, n_changepoints=50, trend_reg=1, weekly_seasonality=False, daily_seasonality=10)
        df_train, df_val = m.split_df(df, freq='H', valid_p = 0.2)
        metrics = m.fit(df_train, freq='H', validation_df=df_val)

        metrics



        future = m.make_future_dataframe(df, periods=24*365*2, n_historic_predictions=len(df))
        forecast = m.predict(future)

        forecast



        forecast.to_csv( "windspeed_prediction.csv", index=False)

        """# <a>Pressure</a>"""

        df = pd.read_csv("datasets/weather_data.csv")[['time_stamp', 'mean_sea_level_pressure']]
        df.time_stamp = pd.to_datetime(df.time_stamp)

        avgpressure = pd.DataFrame(df1.groupby(['date'])['mean_sea_level_pressure'].mean())
        pressure_add = seasonal_decompose(avgpressure['mean_sea_level_pressure'], model='additive',extrapolate_trend='freq',period=365)



        monthlypressure = pd.DataFrame(dfbefore2021.groupby(['month'])['mean_sea_level_pressure'].mean())
        months=['January','February','March','April','May','June','July','August','Sepetember','October','November','December']
        monthlypressure['Month']=months

        df.rename(columns = {'time_stamp':'ds', 'mean_sea_level_pressure':'y'}, inplace = True)

        df['ds'] = pd.DatetimeIndex(df['ds'])
        df.head()





        m = NeuralProphet(changepoints_range=0.95, 
                        n_changepoints=50, 
                        trend_reg=1, 
                        weekly_seasonality=False, 
                        daily_seasonality=10, 
                        yearly_seasonality=10)

        df_train, df_val = m.split_df(df, freq='H', valid_p = 0.2)
        metrics = m.fit(df_train, freq='H', validation_df=df_val)

        metrics

       

        future = m.make_future_dataframe(df, periods=24*365*2, n_historic_predictions=len(df))
        forecast = m.predict(future)

        forecast



        forecast.to_csv( "pressure_prediction.csv", index=False)

        """# <a>Total Cloud Cover</a>"""

        df = pd.read_csv("datasets/weather_data.csv")[['time_stamp', 'total_cloud_cover']]
        df.time_stamp = pd.to_datetime(df.time_stamp)

        avgcloud = pd.DataFrame(df1.groupby(['date'])['total_cloud_cover'].mean())
        cloud_add = seasonal_decompose(avgcloud['total_cloud_cover'], model='additive',extrapolate_trend='freq',period=365)



        monthlycloud = pd.DataFrame(dfbefore2021.groupby(['month'])['total_cloud_cover'].mean())
        months=['January','February','March','April','May','June','July','August','Sepetember','October','November','December']
        monthlycloud['Month']=months


        df.rename(columns = {'time_stamp':'ds', 'total_cloud_cover':'y'}, inplace = True)

        df['ds'] = pd.DatetimeIndex(df['ds'])
        df.head()



        m = NeuralProphet(changepoints_range=0.95, 
                        n_changepoints=50, 
                        trend_reg=1, 
                        weekly_seasonality=False, 
                        daily_seasonality=10, 
                        yearly_seasonality=10)

        df_train, df_val = m.split_df(df, freq='H', valid_p = 0.2)
        metrics = m.fit(df_train, freq='H', validation_df=df_val)

        metrics



        future = m.make_future_dataframe(df, periods=24*365*2, n_historic_predictions=len(df))
        forecast = m.predict(future)

        forecast



        forecast.to_csv( "cloudcover_prediction.csv", index=False)

        temp= pd.read_csv('temperature_prediction.csv')
        cloudcover= pd.read_csv('cloudcover_prediction.csv')
        pressure= pd.read_csv('pressure_prediction.csv')
        wind= pd.read_csv('windspeed_prediction.csv')

        new= temp["ds"].str.split(" ", n = 1, expand = True)
        temp['datestamp'] = pd.to_datetime(temp['ds'])
        temp['date'] = new[0]
        temp['time'] = new[1]
        temp['hour'] = temp['datestamp'].dt.hour

        new= cloudcover["ds"].str.split(" ", n = 1, expand = True)
        cloudcover['datestamp'] = pd.to_datetime(cloudcover['ds'])
        cloudcover['date'] = new[0]
        cloudcover['time'] = new[1]
        cloudcover['hour'] = cloudcover['datestamp'].dt.hour
        cloudcover['date'] = new[0]
        cloudcover['time'] = new[1]

        new= wind["ds"].str.split(" ", n = 1, expand = True)
        wind['datestamp'] = pd.to_datetime(wind['ds'])
        wind['date'] = new[0]
        wind['time'] = new[1]
        wind['hour'] = wind['datestamp'].dt.hour
        wind['date'] = new[0]
        wind['time'] = new[1]

        new= pressure["ds"].str.split(" ", n = 1, expand = True)
        pressure['datestamp'] = pd.to_datetime(pressure['ds'])
        pressure['date'] = new[0]
        pressure['time'] = new[1]
        pressure['hour'] = pressure['datestamp'].dt.hour
        pressure['date'] = new[0]
        pressure['date'] = new[1]

        final =pd.DataFrame()

        final['datestamp'] = temp['datestamp'].astype(str)
        final['date'] = temp['date']
        final['time'] = temp['time']
        final['hour'] = temp['hour']
        final['temperature'] = temp['yhat1']
        final['windspeed'] = wind['yhat1']
        final['pressure'] = pressure['yhat1']
        final['cloudcover'] = cloudcover['yhat1']

        final.to_csv('allpredicted2.csv',index=False)
        x = json.loads(json.dumps(list(final.T.to_dict().values())))
        db.test.insert_many(x)


        return jsonify(message="Model updated successfully")




    @app.route("/login", methods=["POST"])
    def User_Login():
        if request.json['email'] is None:
            return jsonify(msg="All fields are required for logging in", usertype=user['type'], status_code=400)
        
        if  (request.json["password"] == "None") | (request.json["password"] == None):
            return jsonify(msg="All fields are required for logging in",status_code=400)

        email = request.json['email']
        password = request.json["password"]

        # Retrieve a user by email:
        user = db.user.find_one({'username': email})

        # if user is already register show this error message
        if user is None:
            return jsonify({'error': 'User error'}), 401

        if (check_password_hash(user['password'], password))==False:
            return jsonify(msg="Password is incorrect...", status_code=401)

        # session["user_id"] = user['username']
        # print(session['user_id'])
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token, msg="you are Successfully Logged In", usertype=user['type'],status_code=200)


    @jwt_required()
    @app.route("/addstaff", methods=["GET", "POST"])
    def addstaff():
        if request.json['email'] is None:
            return jsonify(msg="All fields are required for Adding a User", usertype=user['type'], status_code=400)
        
        if  (request.json["password"] == "None") | (request.json["password"] == None):
            return jsonify(msg="All fields are required for Adding a User", status_code=400)
        
        # current_user = get_jwt_identity()
        email = request.json['email']
        # email = request.json.get('email', None)
        password = generate_password_hash(request.json["password"])
        # print("hello", password)
        # Retrieve a user by email:
        user = db.user.find_one({'username': email})
        # print(user)
        # if user is already register show this error message

        if user is not None:
            return jsonify(msg = 'User already exists...',status_code = 401 )

        # if user['password'] != password:
        #     return jsonify({'error': 'Password error'}), 401

        # session["user_id"] = user['username']
        # print(session['user_id'])
        # access_token = create_access_token(identity=email)
        db.user.insert_one(
            {'username': email, 'password': password, 'type': 'staff'})

        return jsonify(msg="Staff member added successfully",status_code=200)


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


    @app.route("/tempminmaxavg", methods=['GET'])
    # @jwt_required()
    def tempminmaxavg():

        today = datetime.today().strftime('%Y-%m-%d')

        d = db.allpred.find({'date': today})
        df = pd.json_normalize(d)
        df = df.drop(['_id'], axis=1)
        df = df.sort_values('hour')
        result = {}
        result['temp'] = ({'min': min(df['temperature'].to_list()), 'avg': sum(
            df['temperature'].to_list())/24, 'max': max(df['temperature'].to_list())})
        result['wind'] = {'min': min(df['windspeed'].to_list()), 'avg': sum(
            df['windspeed'].to_list())/24, 'max': max(df['windspeed'].to_list())}
        result['pressure'] = {'min': min(df['pressure'].to_list()), 'avg': sum(
            df['pressure'].to_list())/24, 'max': max(df['pressure'].to_list())}
        result['cloud'] = {'min': min(df['cloudcover'].to_list()), 'avg': sum(
            df['cloudcover'].to_list())/24, 'max': max(df['cloudcover'].to_list())}
        # df =json.loads(json.dumps(list(df.T.to_dict().values())))

        # result={}

        # result['temp']= df['temperature'].to_list()
        # result['date']= df['datestamp'].to_list()
        # result['hour']= df['hour'].to_list()
        # result['wind']= df['windspeed'].to_list()
        # result['press']= df['pressure'].to_list()
        # result['cloud']= df['cloudcover'].to_list()

        return jsonify(result['temp'])


    @app.route("/windminmaxavg", methods=['GET'])
    # @jwt_required()
    def windminmaxavg():

        today = datetime.today().strftime('%Y-%m-%d')

        d = db.allpred.find({'date': today})
        df = pd.json_normalize(d)
        df = df.drop(['_id'], axis=1)
        df = df.sort_values('hour')
        result = {}
        result['temp'] = ({'min': min(df['temperature'].to_list()), 'avg': sum(
            df['temperature'].to_list())/24, 'max': max(df['temperature'].to_list())})
        result['wind'] = {'min': min(df['windspeed'].to_list()), 'avg': sum(
            df['windspeed'].to_list())/24, 'max': max(df['windspeed'].to_list())}
        result['pressure'] = {'min': min(df['pressure'].to_list()), 'avg': sum(
            df['pressure'].to_list())/24, 'max': max(df['pressure'].to_list())}
        result['cloud'] = {'min': min(df['cloudcover'].to_list()), 'avg': sum(
            df['cloudcover'].to_list())/24, 'max': max(df['cloudcover'].to_list())}
        # df =json.loads(json.dumps(list(df.T.to_dict().values())))

        # result={}

        # result['temp']= df['temperature'].to_list()
        # result['date']= df['datestamp'].to_list()
        # result['hour']= df['hour'].to_list()
        # result['wind']= df['windspeed'].to_list()
        # result['press']= df['pressure'].to_list()
        # result['cloud']= df['cloudcover'].to_list()

        return jsonify(result['wind'])


    @app.route("/pressminmaxavg", methods=['GET'])
    # @jwt_required()
    def pressminmaxavg():

        today = datetime.today().strftime('%Y-%m-%d')

        d = db.allpred.find({'date': today})
        df = pd.json_normalize(d)
        df = df.drop(['_id'], axis=1)
        df = df.sort_values('hour')
        result = {}
        result['temp'] = ({'min': min(df['temperature'].to_list()), 'avg': sum(
            df['temperature'].to_list())/24, 'max': max(df['temperature'].to_list())})
        result['wind'] = {'min': min(df['windspeed'].to_list()), 'avg': sum(
            df['windspeed'].to_list())/24, 'max': max(df['windspeed'].to_list())}
        result['pressure'] = {'min': min(df['pressure'].to_list()), 'avg': sum(
            df['pressure'].to_list())/24, 'max': max(df['pressure'].to_list())}
        result['cloud'] = {'min': min(df['cloudcover'].to_list()), 'avg': sum(
            df['cloudcover'].to_list())/24, 'max': max(df['cloudcover'].to_list())}
        # df =json.loads(json.dumps(list(df.T.to_dict().values())))

        # result={}

        # result['temp']= df['temperature'].to_list()
        # result['date']= df['datestamp'].to_list()
        # result['hour']= df['hour'].to_list()
        # result['wind']= df['windspeed'].to_list()
        # result['press']= df['pressure'].to_list()
        # result['cloud']= df['cloudcover'].to_list()

        return jsonify(result['pressure'])


    @app.route("/cloudminmaxavg", methods=['GET'])
    # @jwt_required()
    def cloudminmaxavg():

        today = datetime.today().strftime('%Y-%m-%d')

        d = db.allpred.find({'date': today})
        df = pd.json_normalize(d)
        df = df.drop(['_id'], axis=1)
        df = df.sort_values('hour')
        result = {}
        result['temp'] = ({'min': min(df['temperature'].to_list()), 'avg': sum(
            df['temperature'].to_list())/24, 'max': max(df['temperature'].to_list())})
        result['wind'] = {'min': min(df['windspeed'].to_list()), 'avg': sum(
            df['windspeed'].to_list())/24, 'max': max(df['windspeed'].to_list())}
        result['pressure'] = {'min': min(df['pressure'].to_list()), 'avg': sum(
            df['pressure'].to_list())/24, 'max': max(df['pressure'].to_list())}
        result['cloud'] = {'min': min(df['cloudcover'].to_list()), 'avg': sum(
            df['cloudcover'].to_list())/24, 'max': max(df['cloudcover'].to_list())}
        # df =json.loads(json.dumps(list(df.T.to_dict().values())))

        # result={}

        # result['temp']= df['temperature'].to_list()
        # result['date']= df['datestamp'].to_list()
        # result['hour']= df['hour'].to_list()
        # result['wind']= df['windspeed'].to_list()
        # result['press']= df['pressure'].to_list()
        # result['cloud']= df['cloudcover'].to_list()

        return jsonify(result['cloud'])


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


    @app.route("/getdaypred", methods=['GET'])
    @jwt_required()
    def getdaypred():

        user_id = get_jwt_identity()

        date = request.args.get('date')
        d = db.allpred.find({'date': date})
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

    @app.route("/getcomparison", methods=['GET'])
    @jwt_required()
    def getcomparison():
        user_id = get_jwt_identity()

        date = request.args.get('date')
        aircraft = request.args.get('aircraft')
        print("\n\n\naircraft is", aircraft)

        d = db.allpred.find({'date': date})
        df = pd.json_normalize(d)
        df = df.drop(['_id'], axis=1)
        df = df.sort_values('hour')

        a = db.AirCrafts.find({'Model': aircraft})
        df2 = pd.json_normalize(a)
        df2 = df2.drop(['_id'], axis=1)
        print(df2)

        result = {}

        if ( (result['t_mean'] > result['t_th']) | (result['w_mean'] > result['w_th']) | (result['p_mean'] > result['p_th']) | (result['c_mean'] > result['c_th'])):
            dangered = True
        else:
            dangered = False

        result['data'] = {
            't_mean':  df["temperature"].mean(), 
            'w_mean': df["windspeed"].mean(), 
            'p_mean' : df["pressure"].mean(), 
            'c_mean' : df["cloudcover"].mean(),
            't_th' : df2["Temperature Threshold"].mean(),
            'w_th' : df2["Wind Speed Threshold"].mean(),
            'p_th' : df2["Pressure"].mean(),
            'c_th' : df2["Total Cloud Cover Threshold"].mean(),
            'danger' : dangered
        }

        return jsonify(result['data'])


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
        result['Pressure_t'] = df['Pressure'].to_list()

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

        result = {}
        result['Make'] = make_arr
        result['MakeCount'] = make_count_arr
        result['Categories'] = cat_arr
        result['CategoryCount'] = cat_count_arr
        return jsonify(result)


    @app.route("/aircraftscategories", methods=['GET'])
    def aircraftscategories():

        d = db.AirCrafts.distinct("Model")
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

    @app.route("/check_day_danger", methods=['GET'])
    def check_a_day_danger():
        date = request.args.get('date')
        d = db.allpred.find({'date': date})
        df = pd.json_normalize(d)
        df = df.drop(['_id'], axis=1)
        df = df.sort_values('hour')


        t_mean = df["temperature"].mean()
        w_mean = df["windspeed"].mean()
        p_mean = df["pressure"].mean()
        c_mean = df["cloudcover"].mean()

        print(t_mean, w_mean, p_mean, c_mean)

        aircrafts = db.AirCrafts.find(
            {"$or": [
                {"Temperature Threshold": {"$lte": float(t_mean)}},
                {"Pressure": {"$lte": float(p_mean)}},
                {"Total Cloud Cover Threshold": {"$lte": float(c_mean)}},
                {"Wind Speed Threshold": {"$lte": float(w_mean)}}
            ]},
            {'_id': False}
        )

        df_air = pd.json_normalize(aircrafts)
        result = {}

        for index, row in df_air.iterrows():
            result[index] = dict(row)
        return jsonify(result)



    @app.route("/check_today_danger", methods=['GET'])
    def check_today_danger():

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        new_dt = dt_string[:12] + ":00:00"
        print("\n====================================")
        print("local time:", new_dt)

        wind = db.WindSpeedPred.find_one({"ds": new_dt})
        print("wind predict", wind['yhat1'])

        temp = db.TempPred.find_one({"ds": new_dt})
        print("temp predict", temp['yhat1'])

        cloud = db.CloudCoverPred.find_one({"ds": new_dt})
        print("cloud cover predict", cloud['yhat1'])

        pressure = db.PressurePred.find_one({"ds": new_dt})
        print("pressure predict", pressure['yhat1'])
        print("\n====================================")

        aircrafts = db.AirCrafts.find(
            {"$or": [
                {"Temperature Threshold": {"$lte": float(temp['yhat1'])}},
                {"Pressure": {"$lte": float(pressure['yhat1'])}},
                {"Total Cloud Cover Threshold": {"$lte": float(cloud['yhat1'])}},
                {"Wind Speed Threshold": {"$lte": float(wind['yhat1'])}}
            ]},
            {'_id': False}
        )

        df_air = pd.json_normalize(aircrafts)
        result = {}

        for index, row in df_air.iterrows():
            result[index] = dict(row)
        return jsonify(result)
    return app

if __name__ == '__main__':
    server_init().run(port=5000, debug=True)
