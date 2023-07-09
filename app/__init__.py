from flask import Flask, render_template, redirect, url_for
from app.config import config
from .extensions import moment, lm, bootstrap, db
from app.models.User import User



def create_app(config_name):
    # create app
    app = Flask(__name__)

    # config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # init extentions
    db.init_app(app)
    lm.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    @lm.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # register blue prints
    from app.auth import auth
    app.register_blueprint(auth)

    from app.calculation import calculation
    app.register_blueprint(calculation)

    # index:main page
    @app.route('/')
    def index():
        #return render_template('index.html')
        return redirect(url_for('calculation.my_finance'))


    # errorhandler


    return app