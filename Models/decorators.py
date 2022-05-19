from functools import wraps
from flask import request
import jwt
import os
from dotenv import load_dotenv
load_dotenv()
from Models.UserModel import UserModel

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None
        if 'token' in request.cookies:
            token = request.cookies.get("token")
        elif 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else: return {"Auth-Error":"Token Error"},401

        currentUser=None
        try:
            data = jwt.decode(token,os.getenv('SECRET'),algorithms=["HS256"])
            currentUser=UserModel.find_by_id(data["public_id"])

        except:
           return {"Auth-Error":f"Token Error"},401
        return f(currentUser,*args,**kwargs)
    
    return decorated



