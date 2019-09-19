from flask import render_template, request
from twitoff import db, app
from .models import User, Tweet
from .twitter import add_or_update_user


@app.route('/')
def root():
    users = User.query.all()
    return render_template('base.html', title='Home', users=users)


@app.route('/user', methods=['POST'])
@app.route('/user/<name>', methods=['GET'])
def user(name=None):
    message = ''
    name = name or request.values['user_name']
    try:
        if request.method == 'POST':
            add_or_update_user(name)
            message = 'User {} successfully added!'.format(name)
        tweets = User.query.filter(User.name == name).one().tweets
    except Exception as e:
        message = 'Error adding {}: {}'.format(name, e)
        tweets = []
    return render_template('user.html', title=name, tweets=tweets,
                           message=message)


@app.route('/compare')
def compare(message=''):
    user1, user2 = sorted([request.values['user1'],
                          request.values['user2']])
    if user1 == user2:
        message = 'Cannot compare a user to themselves!'
    else:
        tweet_text = request.values['tweet_text']
        confidence = int(predict_user(user1, user2, tweet_text) * 100)


@app.route('/update')
def update():
    update_all_users()
    return render_template('base.html', title='Update all users!', users=User.query.all())


@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return render_template('base.html', title='DB Reset!', users=[])    
