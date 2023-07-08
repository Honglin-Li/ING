from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
moment = Moment()
bootstrap = Bootstrap()

# login setting
lm = LoginManager()

lm.login_view = 'auth.login'