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
    isPaid = db.Column(db.Boolean, unique=True, nullable=False)


db.create_all()
db.session.commit()


@application.route("/")
def home():
    total = Total.query.filter_by(id=1).first()

    if total == None:
        total = Total(amount=0)
        db.session.add(total)
        db.session.commit()

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
        person11 = request.form["person1"]
        person22 = request.form["person2"]
        amount = request.form["amount"]

        person1 = User.query.filter_by(username=person11).first()
        person2 = User.query.filter_by(username=person22).first()
        total = Total.query.filter_by(id=1).first()

        if (person1.amount + person2.amount) <= total.amount:
            loan = Loan(username=username, person1=person1.username, person2=person2.username, amount=amount,
                        isPaid=False)
            total = Total.query.filter_by(id=1).first()
            total.amount = total.amount - int(amount)

            db.session.add(loan)
            db.session.commit()

            return render_template("dashboard.html")
        else:
            return render_template("requestLoan.html")
    return render_template("requestLoan.html")


@application.route("/pay_loan", methods=["GET", "POST"])
def payLoan():
    if request.method == "POST":
        username = request.form["username"]
        amount = request.form["amount"]

        loan = Loan.query.filter_by(username=username).first()

        if loan.amount == int(amount):
            loan.isPaid = True

            total = Total.query.filter_by(id=1).first()
            total.amount = total.amount + int(amount)
        else:
            return "Payable amount and add amount not match <br/><a href='/pay_loan'>Go Back</a>"

    return render_template("payLoan.html")
