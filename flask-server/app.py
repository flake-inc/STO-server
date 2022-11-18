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

@app.route("/test",methods=['GET'])
# @cross_origin(origin='*',headers=['Content- Type','Authorization'])

def test():

    d = db.user_collection.find({})
    # dict.pop('_id')
    df = pd.json_normalize(d)
    dftempyear = pd.DataFrame(df.groupby(['year'])['temperature'].mean())
    dftempyear['year'] = dftempyear.index

    # tempyear= dftempyear.to_json(orient='records')[1:-1].replace('},{', '} {')
    json_list = json.loads(json.dumps(list(dftempyear.T.to_dict().values())))
    
    # return jsonify(list(d)[0])
    return json_list

if __name__ == '__main__':
    app.run(port=5000,debug=True)

