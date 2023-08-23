from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
from datetime import datetime
import os
from db import db
from models import Form

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///job_applications.db"
    db.init_app(app)

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            applicant = dict(request.form)
            date = {"date": datetime.strptime(request.form["date"], "%Y-%m-%d")}
            form_data = {**applicant, **date}
            form = Form(**form_data)
            db.session.add(form)
            db.session.commit()
            flash(f"Hey {form_data['first_name']}, your application is submitted successfully!", "success")
        return render_template("index.html")

    with app.app_context():
        import models  # noqa: F401

        db.create_all()
    return app
