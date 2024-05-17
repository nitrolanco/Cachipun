from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

SQLALCHEMY_DATABASE_URL = "mysql://root:@localhost:3306/cachipun"
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()