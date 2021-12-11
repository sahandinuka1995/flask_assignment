from flask import Flask, request
from flask.templating import render_template
import os
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)

application.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345678@aaxunchuu0gulp.c8pmpqzflrw9.us-east-1.rds.amazonaws.com:3306/ebdb"
db = SQLAlchemy(application)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    amount = db.Column(db.Integer, unique=True, nullable=False)


class Total(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, unique=True, nullable=False)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    person1 = db.Column(db.String(80), unique=True, nullable=False)
    person2 = db.Column(db.String(80), unique=True, nullable=False)
    amount = db.Column(db.Integer, unique=True, nullable=False)


db.create_all()
db.session.commit()


@application.route("/")
def home():
    return render_template("index.html")


@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        try:
            all = User.query.filter_by(username=username).all()

            for user in all:
                if user.username == username:
                    return render_template("dashboard.html")
        except:
            return render_template("login.html")
    return render_template("login.html")


@application.route("/add_user", methods=["GET", "POST"])
def addUser():
    if request.method == "POST":
        username = request.form["username"]
        amount = request.form["amount"]

        total = Total.query.filter_by(id=1).first()
        total.amount = total.amount + int(amount)

        user = User(username=username, amount=amount)
        db.session.add(user)
        db.session.commit()

    return render_template("index.html")


@application.route("/request_loan", methods=["GET", "POST"])
def requestLoan():
    if request.method == "POST":
        username = request.form["username"]
        person1 = request.form["person1"]
        person2 = request.form["person2"]
        amount = request.form["amount"]

        person1 = User.query.filter_by(username=person1).first()
        person2 = User.query.filter_by(username=person2).first()
        total = Total.query.filter_by(id=1).first()

        if (person1.amount + person2.amount) <= total.amount:
            print('good')
        else:
            print('bad')

    # loan = Loan(username=username, person1=person1, person2=person2, amount=amount)
    # db.session.add(loan)
    # db.session.commit()
    return render_template("requestLoan.html")
