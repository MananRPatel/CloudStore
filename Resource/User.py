from flask_restful import Resource, reqparse
from flask import Flask, make_response, request
from Models.UserModel import UserModel
import os
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import datetime

load_dotenv()


class User_Register(Resource):

    _user_parser = reqparse.RequestParser()
    _user_parser.add_argument('username',
                              type=str,
                              required=True,
                              help="This field cannot be blank.")
    _user_parser.add_argument('email',
                              type=str,
                              required=True,
                              help="This field cannot be blank.")
    _user_parser.add_argument('password',
                              type=str,
                              required=True,
                              help="This field cannot be blank.")

    @classmethod
    def post(cls):

        data = cls._user_parser.parse_args()

        if UserModel.find_by_mail(data['email']):
            return {"message": "A user with that username already exists"}, 400

        data['password'] = generate_password_hash(data['password'],
                                                  method='sha256')
        user = UserModel(**data)
        user.save_to_db()

        token = jwt.encode(
            {
                'public_id': user.id,
                'exp': datetime.datetime.now() + datetime.timedelta(days=15)
            }, os.getenv('SECRET'))

        res = make_response({"token": token})
        res.status_code = 201
        res.set_cookie("token",
                       value=token,
                       expires=(datetime.datetime.now() +
                                datetime.timedelta(days=15)))

        return res


class User_Login(Resource):

    _user_parser = reqparse.RequestParser()
    _user_parser.add_argument('email',
                              type=str,
                              required=True,
                              help="This field cannot be blank.")

    _user_parser.add_argument('password',
                              type=str,
                              required=True,
                              help="This field cannot be blank.")

    @classmethod
    def post(cls):

        data = cls._user_parser.parse_args()
        user = UserModel.find_by_mail(data['email'])
        if not user:
            return {"Error": "Wrong Credentials"}, 401

        if check_password_hash(user.password, data['password']):
            token = jwt.encode(
                {
                    'public_id': user.id,
                    'exp':
                    datetime.datetime.now() + datetime.timedelta(days=15)
                }, os.getenv('SECRET'))

            res = make_response({"token": token})
            res.status_code = 201
            res.set_cookie("token",
                           value=token,
                           expires=(datetime.datetime.now() +
                                    datetime.timedelta(days=15)))
            return res
        return {"Error": "Wrong Credentials"}, 401
