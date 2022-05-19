from flask_restful import Resource
from Models.CloudModel import CloudModel

class Cloud(Resource):

    @classmethod
    def get(cls):
        user = CloudModel(1,"1223dwdssd","dsdsd","owner")
        #user.save_to_db()
        print("dfdfdfdfd\n\n\\n\n\\n\n\n\\n\n\\n\n\n\n\n\n\n")
        print(user.find_by_id(1).json())
        return "done"