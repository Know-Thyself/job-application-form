from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
from models import Form
from datetime import datetime
from flask_mail import Mail, Message
from db import db
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///job_applications.db"
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    db.init_app(app)
    mail = Mail(app)

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            applicant = dict(request.form)
            date = {"date": datetime.strptime(request.form["date"], "%Y-%m-%d")}
            form_data = {**applicant, **date}
            form = Form(**form_data)
            db.session.add(form)
            db.session.commit()
            message_body = f"Thank you for your application, {form_data['first_name']}!"
            message = Message(
                subject="Form Submission Confirmation",
                sender=app.config["MAIL_USERNAME"],
                recipients=[applicant["email"]],
                body=message_body,
            )
            mail.send(message)
            flash(
                f"Hey {form_data['first_name']}, your application is submitted successfully!",
                "success",
            )
        return render_template("index.html")

    with app.app_context():
        import models  # noqa: F401

        db.create_all()
    return app
