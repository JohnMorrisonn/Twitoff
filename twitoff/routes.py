from flask import render_template
from twitoff import db, app
from .models import User, Tweet

@app.route("/")

def home():
    users = User.query.all()
    return render_template('base.html', title = 'Home', users=users)


@app.route("/about")

def pred():
    return render_template('about.html')