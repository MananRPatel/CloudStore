from db import db
from Models.IdentityModel import IdentityModel
import os

class CloudModel(db.Model):
    __tablename__ = 'cloud'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    file_id = db.Column(db.String(100), db.ForeignKey('files.id'))
    owner_id = db.Column(db.Integer,db.ForeignKey('identity.id',ondelete="CASCADE"),default=None)
    filename = db.Column(db.String(80))
    roll = db.Column(db.String(10))

    def __init__(self, user_id, file_id, filename, roll, owner_id=None):
        self.user_id = user_id
        self.file_id = file_id
        self.filename = filename
        self.roll = roll
        self.owner_id = owner_id

    def json(self):
        return {'filename': self.filename, 'roll': self.roll}

    def share_json(self):
        return {'email': self.cloudier.email, 'roll': self.roll}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(user_id=_id)

    @classmethod
    def find_by_fileName(cls, name):
        return cls.query.filter_by(filename=name).first()
    
    @classmethod
    def find_owner(cls, userId,fileName):
        return cls.query.filter_by(filename=fileName,user_id=userId,owner_id=None).first()


    @classmethod
    def createFriends(cls, owner_id, cloud_data, friends):
        ownership =  IdentityModel.get_id(owner_id, cloud_data.filename).id
        for i in friends:
            CloudModel(i, cloud_data.file_id, cloud_data.filename, "friends",
                      ownership).save_to_db()

    @classmethod
    def removeFriends(cls, owner_id_, cloud_data, friends_ids):
        for i in friends_ids:
            cls.query.filter_by(filename=cloud_data.filename,user_id=i,owner_id= IdentityModel.get_id(owner_id_,cloud_data.filename).id).delete()
            db.session.commit()

    @classmethod
    def updatePower(cls,owner_id_, cloud_data, friends_id):


       owner_data = cls.find_owner(owner_id_,cloud_data.filename)

       identityOwnerData = IdentityModel.get_id(owner_id_,cloud_data.filename)

       friend_data = cls.find_friend(owner_id_,cloud_data.filename,friends_id)

       owner_data.owner_id=identityOwnerData.id
       owner_data.roll="friends"
       friend_data.owner_id=None
       identityOwnerData.owner_id=friends_id
       friend_data.roll="Owner"

       db.session.commit()

    @classmethod
    def deleteFile(cls,id_,filename_):

        cloudData = cls.find_owner(id_,filename_)

        if cloudData is None:return False


        realFileName = cloudData.file_id
        IdentityModel.get_id(id_,filename_).delete_from_db()
        cloudData.delete_from_db()
        os.remove(f"DataBlock\\{realFileName}")
        return True
    
    #for retrieve single user
    @classmethod
    def find_friend(cls, owner_id_,fileName,userID):
        realOwner = IdentityModel.get_id(owner_id_,fileName)
        if realOwner == None: return None
        return cls.query.filter_by(filename=fileName,user_id=userID,owner_id=realOwner.id).first()
    
    #for all friends
    @classmethod
    def find_all_users(cls,id,file_name):
        realOwner = IdentityModel.get_id(id,file_name)
        if realOwner == None: return None
        return cls.query.filter_by(filename=file_name,owner_id=realOwner.id)
