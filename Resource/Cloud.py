from flask_restful import Resource, reqparse
from Models.CloudModel import CloudModel
from Models.FileModel import FileModel
from Models.IdentityModel import IdentityModel
from Models.decorators import token_required
from flask import request, send_file
import hashlib
import os
import shutil


class Cloud_myDrive(Resource):

    @classmethod
    @token_required
    def get(currentUser, cls):
        filename = request.args.get('filename')
        cloudData = CloudModel.find_by_fileName(filename)
        if cloudData is None: return {"Error": "No File found"}, 404
        return send_file(f"DataBlock\\{cloudData.file_id}", as_attachment=True)

    @classmethod
    @token_required
    def post(currentUser, cls):

        fileName = request.form.get("filename")
        if fileName == None: return {"Error": "No file name provided"}, 404

        fileData = request.files.get("file", "")
        if fileData == None: return {"Error": "No file uploaded"}, 404

        fileData.save(f"Temp\\{currentUser.id}{fileName}")
        fileSize = os.stat(f"Temp\\{currentUser.id}{fileName}").st_size

        if fileSize > 20 * 1024 * 1024:
            return {"Error": "File size is too large"}

        openedFile = open(f"Temp\\{currentUser.id}{fileName}", "rb")
        readFile = openedFile.read()
        sha256Hashed = hashlib.sha256(readFile).hexdigest()
        openedFile.close()

        if CloudModel.find_by_fileName_with_ownership(currentUser.id,fileName):
            return {
                "Error":
                "Filename already exist please provide other file name to identify the file"
            }, 400

        if FileModel.getHash(sha256Hashed):

            cloud = CloudModel(currentUser.id, sha256Hashed, fileName, "Owner")
            IdentityModel(currentUser.id, fileName).save_to_db()
            os.remove(f"Temp\\{currentUser.id}{fileName}")

        else:

            shutil.move(f"Temp\\{currentUser.id}{fileName}",
                        f"DataBlock\\{sha256Hashed}")

            fileStorage = FileModel(sha256Hashed, fileSize)
            fileStorage.save_to_db()

            IdentityModel(currentUser.id, fileName).save_to_db()

            cloud = CloudModel(currentUser.id, fileStorage.id, fileName,
                               "Owner")

        cloud.save_to_db()

        return cloud.json()

    @classmethod
    @token_required
    def delete(currentUser, cls):

        _user_parser = reqparse.RequestParser()
        _user_parser.add_argument('filename',
                                  type=str,
                                  required=True,
                                  help="please add your file name")

        data = _user_parser.parse_args()

        if CloudModel.deleteFile(currentUser.id, data['filename']):
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
    @token_required
    def get(currentUser, cls):
        return {
            "Data":
            [i.json() for i in CloudModel.find_by_user_id(currentUser.id)]
        }

    @classmethod
    @token_required
    def post(currentUser, cls):
        data = _user_parser.parse_args()

        cloud_data = CloudModel.find_by_fileName(data['filename'])
        if cloud_data is None: return {"Error": "File does not exists"}, 404
        CloudModel.createFriends(currentUser.id, cloud_data, data['friends'])
        return {"Message": "Shared file to all friends"}, 201

    @classmethod
    @token_required
    def delete(currentUser, cls):
        data = _user_parser.parse_args()
        cloud_data = CloudModel.find_by_fileName(data['filename'])
        if cloud_data is None: return {"Error": "File does not exists"}, 404
        CloudModel.removeFriends(currentUser.id, cloud_data, data['friends'])
        return {"Message": f"Remove Friends {data['filename']}"}, 200

    @classmethod
    @token_required
    def put(currentUser, cls):
        data = _user_parser.parse_args()
        cloud_data = CloudModel.find_by_fileName(data['filename'])
        if cloud_data is None: return {"Error": "File does not exists"}, 404
        CloudModel.updatePower(currentUser.id, cloud_data, data['friends'][0])
        return {"Message": "Power changed"}, 200


class CloudShare(Resource):

    @classmethod
    @token_required
    def get(currentUser, cls, filename):

        
        listOfFriends = CloudModel.find_all_users(currentUser.id, filename)

        if listOfFriends is None: return {"Error": "No Friends found"}

        return {"File": [i.share_json() for i in listOfFriends]}
