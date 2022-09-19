
from flask import Flask

app = Flask(__name__)

# Main function
@app.route('/')
def home():
    return 'You are directed to the home page!'

@app.route('/about')
def about():
    return 'You are directed to the about page!'

if __name__ == '__main__':
    app.run()