from app import app, socketio, db
from flask import render_template, flash, redirect, url_for
from flask_socketio import send
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Message, get_previous_messages
from app.forms import RegistrationForm, LoginForm
from app.stats import average_words_in_message, user_activity, time_stat
from datetime import datetime
from app.errors import *

@app.route('/')
def index():
    return render_template('indexx.html')

@app.route('/stats')
def stats():
    AWiM = average_words_in_message()
    UA = user_activity()
    TS = time_stat()
    return render_template('stats.html',av_words=AWiM,user_activity=UA,time_stats=TS)

@app.route('/chat')
@login_required
def chat():
    for_sending = []
    for i in get_previous_messages():
        for_sending.append([(User.query.filter_by(id = i.user_id).first().username),i.body])
        #print(Message.query.order_by(Message.id.desc()).all())

        #handleMessage(for_sending, broadcast=True)
    for_sending = for_sending[::-1]
    return render_template('chat.html',previous_messages=for_sending)

@socketio.on('message')
def handleMessage(msg):
    if current_user.is_authenticated:
        cur_time = str(datetime.now().strftime('%H:%M:%S'))
        msg_user = [current_user.username,msg,cur_time]
        message = Message(body=msg, user_id=current_user.id)
        if message.body != ' has connected!':
            db.session.add(message)
            print(message.body)
        db.session.commit()
        #print(msg_user)
        send(msg_user, broadcast=True)
    else:
        print('Message: ' + msg)
        send(msg, broadcast=True)

"""@socketio.on('connect')
def handleConnect():
    user = current_user
    print('User that connected: ', user)
    send(user, broadcast=True)
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('chat'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('chat'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
