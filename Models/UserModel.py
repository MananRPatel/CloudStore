from db import db
from Models.CloudModel import CloudModel

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))

    cloudUser = db.relationship('CloudModel',backref='cloudier')

    def __init__(self, username,email, password):
        self.username = username
        self.email= email
        self.password = password
    
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

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
    def find_by_mail(cls, _mail):
        return cls.query.filter_by(email=_mail).first()