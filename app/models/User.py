from datetime import datetime
from app.extensions import db, lm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin


class AnonymousUser(AnonymousUserMixin):
    pass


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    def __repr__(self):
        return f'<User {self.username}>'

    # columns of auth
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    last_seen = db.Column(db.DateTime)
    lock = db.Column(db.Boolean, default=False)

    # personal information
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    birthday = db.Column(db.Date)
    is_married = db.Column(db.Boolean, default=False)

    # partner & share
    partner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    partner = db.relationship('User', uselist=False)
    share = db.Column(db.Boolean, default=False)

    # finance info
    # assume one person only has one fee form, so put fee in user table
    #fee_details = db.relationship('Fee', backref='owner', uselist=False)
    # income
    salary = db.Column(db.Integer, default=0) # consider tax
    external_income = db.Column(db.Integer, default=0)

    # expense
    rent = db.Column(db.Integer, default=0)
    load = db.Column(db.Integer, default=0)
    travel = db.Column(db.Integer, default=0)
    insurance = db.Column(db.Integer, default=0)
    education = db.Column(db.Integer, default=0)
    personal_care = db.Column(db.Integer, default=0)

    # by hour
    childcare = db.Column(db.Integer, default=0)
    household = db.Column(db.Integer, default=0)

    childcare_hours = db.Column(db.Integer, default=0)
    household_hours = db.Column(db.Integer, default=0)

    # handle hashed password
    @property
    def password(self):
        raise AttributeError('password property can not be be accessed')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # partner connection
    def connect(self, partner):
        self.partner = partner






