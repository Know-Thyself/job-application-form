from db import db


class Form(db.Model):
    __tablename__ = "job_application_forms"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    occupation = db.Column(db.String, nullable=False)
