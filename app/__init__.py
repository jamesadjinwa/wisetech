from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
# login = LoginManager()
# login.login_view = 'auth.login'
# login.login_message = _l('Please log in to access this page')
# mail = Mail()
# bootstrap = Bootstrap()
# moment = Moment()
# babel = Babel()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    # login.init_app(app)
    # mail.init_app(app)
    # bootstrap.init_app(app)
    # moment.init_app(app)
    # babel.init_app(app)
    

    # register errors blueprint with app
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # register authentication blueprint with app
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app import routes, models