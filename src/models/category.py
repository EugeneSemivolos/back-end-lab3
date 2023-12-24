from ..db import db


class categoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(128), unique = True, nullable = False)

    record = db.relationship("recordModel", back_populates = "category", lazy = "dynamic")