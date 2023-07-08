from app import create_app
from app.models.User import User
from app.extensions import db


app = create_app(config_name='dev')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


if __name__ == '__main__':
    app.run()