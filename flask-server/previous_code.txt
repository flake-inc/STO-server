
from flask import Flask, render_template, request, url_for, redirect
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from pymongo import MongoClient
from flask import jsonify
import pandas as pd

app = Flask(__name__)
CORS(app)

client = MongoClient('localhost', 27017)
db = client["SafeTakeOff"]
sto = db["Weather"]
# print("Read Here")
# print(client.server_info())
print(sto.find_one())


@app.route('/summary', methods=['GET', 'OPTIONS'])
def get_summary():
    dict = sto.find_one()
    dict.pop('_id')
    return jsonify(dict)

df = pd.read_csv('./weather_data.csv')

# Main function
@app.route('/', methods=('GET', 'POST'))
def home():
    # return 'You are directed to the home page!'
    return redirect('http://127.0.0.1:5173/')


@app.route('/dataframe', methods=['GET'])
def get_dataframe():
    # return 'You are directed to the home page!'
    with open("./weather_data.csv") as f:
            file_content = f.read()

    return file_content 

if __name__ == '__main__':
    app.run()