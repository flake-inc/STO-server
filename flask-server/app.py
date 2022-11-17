from flask import Flask

import db
#test to insert data to the data base

app = Flask(__name__)

@app.route('/')
def flask_mongodb_atlas():
    return "flask mongodb atlas!"

@app.route("/test")
def test():
    db.db.test.insert_one({"name": "John"})
    return "Connected to the data base!"

if __name__ == '__main__':
    app.run(port=8000,debug=True)

