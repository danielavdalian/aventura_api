from db import db

class TributoModel(db.Model):
    __tablename__  = "tributos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
   