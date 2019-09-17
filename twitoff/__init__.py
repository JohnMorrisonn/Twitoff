from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')

#stop tracking mods
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['ENV'] = config('ENV')

db = SQLAlchemy(app)

from twitoff import routes