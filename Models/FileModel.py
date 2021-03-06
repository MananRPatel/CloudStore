from db import db
from Models.CloudModel import CloudModel

class FileModel(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.String(100), primary_key=True)
    filesize = db.Column(db.Integer)

    files = db.relationship('CloudModel',backref='docs')

    def __init__(self,id,filesize):
        self.id = id
        self.filesize = filesize
    
    def json(self):
        return {
            'filesize': self.filesize
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def getHash(cls, _id):
        return cls.query.filter_by(id=_id).first()
