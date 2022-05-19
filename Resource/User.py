from flask_restful import Resource
from Models.UserModel import UserModel

class User(Resource):

    @classmethod
    def get(cls):
        user = UserModel("Tester","Data@data.com",12345678)
       # user.save_to_db()
        print("dfdfdfdfd\n\n\\n\n\\n\n\n\\n\n\\n\n\n\n\n\n\n")
        print(user.find_by_mail(user.email).json())
        return "done"