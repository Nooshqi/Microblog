#set init file so that the website application exists in a package(allowing it to be imported)
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from flask_mail import Mail
from flask_bootstrap import Bootstrap

#declare the appropriate instances: Flask, database, db migration
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail=Mail(app)
bootstrap=Bootstrap(app)

#set view function that handles login, for flask_login functionality @login_required 
login = LoginManager(app)
login.login_view = 'login'

#avoiding circular imports
from app import routes, models, errors

### Chap7 of book talks of shifting how you receive the logs, keen if you debugging production server (Way of managing server up time)