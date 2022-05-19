from db import db

class IdentityModel(db.Model):
    __tablename__ = 'identity'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    filename = db.Column(db.String(80))

    permissions = db.relationship('CloudModel',backref='permits',cascade="save-update")

    def __init__(self,id,filename):
        self.owner_id = id
        self.filename = filename
    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_id(cls,ownerId,fileName):
        return cls.query.filter_by(owner_id=ownerId,filename=fileName).first()

