from db import db

class TributoModel(db.Model):
    __tablename__  = "tributos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    district = db.Column(db.Integer, nullable=False)
    total_points = db.Column(db.Integer, nullable=False, default = 0)
    img_src = db.Column(db.String(80), unique=False, nullable=False)