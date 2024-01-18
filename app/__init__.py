from logging import Manager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
manager = LoginManager(app)
manager.login_view = 'login'  


from app import routes, models, auth 
