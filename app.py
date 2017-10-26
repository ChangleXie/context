# -*- coding:utf-8 -*-

import random
from flask import Flask, g, render_template
from ext import db
from users import User

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


def get_current_user():
    users = User.query.all()
    return random.choice(users)


@app.before_first_request
def setup():
    db.drop_all()
    db.create_all()
    fake_users = [
        User('xiaoming', 'xiaoming@gmial.com'),
        User('lilei', 'lilei@gmail.com'),
        User('hanmeimei', 'hanmeimei@gmail.com')
    ]

    db.session.add_all(fake_users)
    db.session.commit()


@app.before_request
def before_request():
    g.user = get_current_user()


@app.teardown_appcontext
def teardown(ext=None):
    if ext is None:
        db.session.commit()
    else:
        db.session.rollback()
    db.session.remove()
    g.user = None

@app.context_processor
def template_extras():
    return {'enumerate': enumerate, 'current_user': g.user}

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

@app.template_filter('capitalize')
def reverse_filter(s):
    return s.capitalize


@app.route('/users')
def user_view():
    users = User.query.all()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run()
