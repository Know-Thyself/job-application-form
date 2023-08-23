from flask import Flask, render_template, request
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
            date_obj = datetime.strptime(request.form["date"], "%Y-%m-%d")
            # Inserting data to the form table
            form = Form(
                first_name=request.form["first_name"],
                last_name=request.form["last_name"],
                email=request.form["email"],
                date=date_obj,
                occupation=request.form["occupation"],
            )
            db.session.add(form)
            db.session.commit()
        return render_template("index.html")

    with app.app_context():
        import models  # noqa: F401

        db.create_all()
    return app
