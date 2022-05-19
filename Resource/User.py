from flask_restful import Resource,reqparse
from Models.UserModel import UserModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )


class User(Resource):

    @classmethod
    def get(cls,id):
        return UserModel.find_by_id(id).json()

    @classmethod
    def post(cls,id):
        data = _user_parser.parse_args()

        if UserModel.find_by_mail(data['email']):
            return {"message": "A user with that username already exists"}, 400
        
        user = UserModel(**data)
        user.save_to_db()
        return {"data": user.json()}, 201