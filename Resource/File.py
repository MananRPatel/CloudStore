from flask_restful import Resource
from Models.FileModel import FileModel

class File(Resource):

    @classmethod
    def get(cls):
        user = FileModel("1223dwdssd","Dsds",122)
        #user.save_to_db()
        print("dfdfdfdfd\n\n\\n\n\\n\n\n\\n\n\\n\n\n\n\n\n\n")
        print(user.find_by_id(user.id).json())
        return "done"