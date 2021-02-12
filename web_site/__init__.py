from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

data_base = SQLAlchemy()

def create_site():
    web_site = Flask(__name__)

    from .auth import auth
    from .home import home
    web_site.register_blueprint(home, url_prefix='/')
    web_site.register_blueprint(auth, url_prefix='/')

    web_site.secret_key = 'secret4523A#Abn'
    web_site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
    web_site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    data_base.init_app(web_site)
    data_base.create_all(app=web_site)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(web_site)

    from .models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return web_site
