from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')
app.secret_key = 'secret-key'
db = SQLAlchemy(app)

from app import views, models
