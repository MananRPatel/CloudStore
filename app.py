from flask import Flask
from flask_restful import ResourceApi

app = Flask(__name__)
api = Api(app)

class Test(Resource):
    @classmethod
    def get(cls):
        return "World!"

api.add_resource(Test,'/')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
