from db import db

class CloudModel(db.Model):
    __tablename__ = 'cloud'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    file_id = db.Column(db.String(100), db.ForeignKey('files.id'))
    filename = db.Column(db.String(80))
    roll = db.Column(db.String(10))
    owner_id = db.Column(db.Integer, default=None)

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
    def createFriends(cls, owner_id, cloud_data, friends):
        for i in friends:
            CloudModel(i, cloud_data.file_id, cloud_data.filename, "friends",
                       owner_id).save_to_db()

    
    @classmethod
    def find_all_users(cls,id,file_name):
        return cls.query.filter_by(filename=file_name,owner_id=id).all()
