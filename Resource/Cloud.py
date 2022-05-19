from flask_restful import Resource, reqparse
from Models.CloudModel import CloudModel
from Models.FileModel import FileModel
from flask import request,send_file
import hashlib
import os
import shutil

class Cloud(Resource):

    @classmethod
    def get(cls, id):
        for i in CloudModel.find_by_user_id(id):
            print(i.json())
        return "Done"

    @classmethod
    def post(cls, id):

        fileName=request.form.get("filename")
        if fileName == None: return {"Error":"No file name provided"},404
        fileData = request.files.get("file","")
        if fileData == None: return {"Error":"No file uploaded"},404

        
        fileData.save(f"Temp\\{id}{fileName}")

        openedFile = open(f"Temp\\{id}{fileName}","rb")
        readFile = openedFile.read()


        sha256Hashed = hashlib.sha256(readFile).hexdigest()
        openedFile.close()
        
#        return send_file('testfile.png',as_attachment=True)

        if FileModel.getHash(sha256Hashed):
            cloud = CloudModel(id, sha256Hashed, fileName, "Owner")
            os.remove(f"Temp\\{id}{fileName}")
        else:
            shutil.move(f"Temp\\{id}{fileName}",f"DataBlock\\{sha256Hashed}")
            fileStorage = FileModel(sha256Hashed,fileName, 1000)
            fileStorage.save_to_db()
            cloud = CloudModel(id, fileStorage.id,fileName, "Owner")
        cloud.save_to_db()
        return cloud.json()
