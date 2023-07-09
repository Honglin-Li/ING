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
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    last_seen = db.Column(db.DateTime)
    lock = db.Column(db.Boolean, default=False)

    # personal information
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    is_married = db.Column(db.Boolean, default=False)

    # partner & share
    partner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    partner = db.relationship('User', uselist=False)
    share = db.Column(db.Boolean, default=False)

    # finance info
    # income
    salary = db.Column(db.Integer, default=0) # consider tax
    salary_per_hour = db.Column(db.Integer, default=0)

    # career life balance
    goal = db.Column(db.Boolean, default=0) # 0 for priorize mone, 1 for life
    working_hours_a_day = db.Column(db.Integer, default=0)
    life_hours_a_day = db.Column(db.Integer, default=0)
    care_hours_a_day = db.Column(db.Integer, default=0)

    @property
    def job_composition(self):
        return self.working_hours_a_day * 5 / 40

    # expense
    expenses_contribution = db.Column(db.Integer, default=0)

    house_care_hours_per_day = db.Column(db.Integer, default=0)

    @property
    def house_care_hours(self):
        return self.house_care_hours_per_day * 30

    # by hour
    outsource_house_care_hours = db.Column(db.Integer, default=0)

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








