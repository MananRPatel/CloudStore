from flask_restful import Resource, reqparse
from Models.CloudModel import CloudModel
from Models.FileModel import FileModel
from Models.IdentityModel import IdentityModel
from flask import request, send_file
import hashlib
import os
import shutil


class Cloud_myDrive(Resource):

    @classmethod
    def get(cls, info):
        name = info
        cloudData = CloudModel.find_by_fileName(name)
        return send_file(f"DataBlock\\{cloudData.file_id}", as_attachment=True)

    @classmethod
    def post(cls, info):
        user_id = info
        fileName = request.form.get("filename")
        if fileName == None: return {"Error": "No file name provided"}, 404
        fileData = request.files.get("file", "")
        if fileData == None: return {"Error": "No file uploaded"}, 404
        filesize = fileData.content_length
        fileData.save(f"Temp\\{user_id}{fileName}")

        openedFile = open(f"Temp\\{user_id}{fileName}", "rb")
        readFile = openedFile.read()

        sha256Hashed = hashlib.sha256(readFile).hexdigest()
        openedFile.close()

        if CloudModel.find_by_fileName(fileName):
            return {
                "Error":
                "Filename already exist please provide other file name to identify the file"
            }, 400

        if FileModel.getHash(sha256Hashed):
            cloud = CloudModel(user_id, sha256Hashed, fileName, "Owner")
            os.remove(f"Temp\\{user_id}{fileName}")
        else:
            shutil.move(f"Temp\\{user_id}{fileName}",
                        f"DataBlock\\{sha256Hashed}")
            fileStorage = FileModel(sha256Hashed, filesize)
            fileStorage.save_to_db()
            IdentityModel(user_id, fileName).save_to_db()
            cloud = CloudModel(user_id, fileStorage.id, fileName, "Owner")
        cloud.save_to_db()
        return cloud.json()

    @classmethod
    def delete(cls, info):
        id = info

        _user_parser = reqparse.RequestParser()
        _user_parser.add_argument('filename',
                                  type=str,
                                  required=True,
                                  help="please add your file name")

        data = _user_parser.parse_args()

        if CloudModel.deleteFile(id, data['filename']):
            return {"Success": True}
        return {"Error": "Delete on file don't work"}, 404


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('filename',
                          type=str,
                          required=True,
                          help="please add your file name")
_user_parser.add_argument(
    'friends',
    type=int,
    action='append',
    help=
    "This field cannot be blank or contain list also when single friend contain."
)


class CloudPermission(Resource):

    @classmethod
    def get(cls, id):
        return {"Data": [i.json() for i in CloudModel.find_by_user_id(id)]}

    @classmethod
    def post(cls, id):
        data = _user_parser.parse_args()

        cloud_data = CloudModel.find_by_fileName(data['filename'])
        if cloud_data is None: return {"Error": "File does not exists"}, 404
        CloudModel.createFriends(id, cloud_data, data['friends'])
        return {"Message": "Shared file to all friends"}, 201

    @classmethod
    def delete(cls, id):
        data = _user_parser.parse_args()
        cloud_data = CloudModel.find_by_fileName(data['filename'])
        if cloud_data is None: return {"Error": "File does not exists"}, 404
        CloudModel.removeFriends(id, cloud_data, data['friends'])
        return {"Message": f"Remove Friends {data['filename']}"}, 200

    @classmethod
    def put(cls, id):
        data = _user_parser.parse_args()
        cloud_data = CloudModel.find_by_fileName(data['filename'])
        print(data['friends'][0], cloud_data)
        if cloud_data is None: return {"Error": "File does not exists"}, 404
        CloudModel.updatePower(id, cloud_data, data['friends'][0])
        return {"Message": "Power changed"}, 200


class CloudShare(Resource):

    @classmethod
    def get(cls, id, filename):
        return {
            "File":
            [i.share_json() for i in CloudModel.find_all_users(id, filename)]
        }
