from flask import render_template, request
from twitoff import db, app
from .models import User, Tweet
from .twitter import add_or_update_user, update_all_users, add_users
from .predict import predict_user


@app.route('/')
def root():
    users = User.query.all()
    return render_template('base.html', title="Who's It Going to Be?", users=users)


@app.route('/bulma')
def bulma():
    return render_template('bulma_base.html')


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


@app.route('/compare', methods=['POST'])
def compare(message=''):
    user1, user2 = sorted([request.values['user1'],
                          request.values['user2']])
    if user1 == user2:
        message = 'Cannot compare a user to themselves!'
        return render_template('prediction.html', title='Prediction', message=message)
    else:
        tweet_text = request.values['tweet_text']
        confidence = int(predict_user(user1, user2, tweet_text) * 100)
        if confidence >= 50:
            message = f'"{tweet_text}" is more likely to be said by {user1} than {user2}, with {confidence}% confidence'
        else:
            message = f'"{tweet_text}" is more likely to be said by {user2} than {user1}, with {100-confidence}% confidence'
        return render_template('prediction.html', title='Prediction', message=message)

@app.route('/update')
def update():
    update_all_users()
    return render_template('base.html', title='Update all users!', users=User.query.all())
    

@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return render_template('base.html', title='DB Reset!', users=[])    
