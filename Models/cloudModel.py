from db import db

class CloudModel(db.Model):
    __tablename__ = 'cloud'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    file_id = db.Column(db.String(100), db.ForeignKey('files.id'))
    filename = db.Column(db.String(80))
    roll = db.Column(db.String(10))
    

    def __init__(self,user_id,file_id,filename,roll):
        self.user_id = user_id
        self.file_id = file_id
        self.filename = filename
        self.roll = roll
    
    def json(self):
        return {
            'filename': self.filename,
            'roll': self.roll,
            'email':self.cloudier.password
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

    
