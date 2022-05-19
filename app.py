from flask import Flask
from flask_restful import Api
from Resource.User import User
from db import db
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
api = Api(app)


host = os.getenv('HOST')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def root():
    return {"Welcome":"Welcome to Cloud Storage"}

api.add_resource(User,'/user')

@app.errorhandler(404)
def not_found(e):

  return {"Error":"No Route"}

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
