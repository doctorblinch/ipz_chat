from app import app, socketio, db
from flask import render_template, flash, redirect, url_for, jsonify
from flask_socketio import send
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Message, get_previous_messages, Chat, chats_users
from app.forms import RegistrationForm, LoginForm, AddChatForm
from app.stats import average_words_in_message, user_activity, time_stat
from datetime import datetime
from app.errors import *
import speech_recognition as sr
import pyaudio

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
def chat():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    for_sending = []
    for i in get_previous_messages():
        for_sending.append([(User.query.filter_by(id = i.user_id).first().username),i.body])
        #print(Message.query.order_by(Message.id.desc()).all())for_sending.append([(User.query.filter_by(id = i.user_id).first().username),i.body])

        #handleMessage(for_sending, broadcast=True)
    for_sending = for_sending[::-1]
    return render_template('chat.html',previous_messages=for_sending)


def voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said : {}".format(text))
            return text
        except:
            print("Sorry could not recognize what you said")
    return ''


@socketio.on('message')
def handleMessage(msg):
    if current_user.is_authenticated:
        cur_time = str(datetime.now().strftime('%H:%M:%S'))
        msg_user = [current_user.username,msg[0],cur_time]

        chat_id = (msg[1].split('/'))[-1]
        #print(chat_id)
        if msg[0] == 'voice message':
            print('\n\n\nVOICE\n\n\n')
            msg[0] = voice()
            if msg[0] != '':
                msg_user = [current_user.username,msg[0],cur_time]
        message = Message(body=msg[0], user_id=current_user.id, chat_id=chat_id)
        if message.body != ' has connected!':
            db.session.add(message)
            print(message.body)
        db.session.commit()
        #print(msg_user)
        send(msg_user, broadcast=True)
    else:
        print('Message: ' + msg[0])
        send(msg[0], broadcast=True)

@app.route('/chat_id/<id>')
def chat_id(id):
    this_chat = Chat.query.filter_by(id=id).first()
    if current_user in this_chat.users:
        for_sending = []
        for i in get_previous_messages(chat_id=id):
            for_sending.append([(User.query.filter_by(id = i.user_id).first().username),i.body])
        for_sending = for_sending[::-1]
        return render_template('chat.html',previous_messages=for_sending)
    else:
        return '<a href=/><h1>Go away!</h1></a>'


@app.route('/create_new_chat', methods=['GET','POST'])
def create_new_chat():
    form = AddChatForm()
    if form.validate_on_submit():
        users = form.users.data
        print('\n\n\nUsers are:',users,'\n\n\n')
        for user in users.split(' '):
            print(user)
            if (User.query.filter_by(username=user).first()) is None:
                flash('Invalid users selected')
                return redirect(url_for('chat'))
        users = users.split(' ')
        u = []
        for user in users:
            u.append(User.query.filter_by(username=user).first())
        chat = Chat(name=form.name.data, users=u)
        print(chat)
        db.session.add(chat)
        db.session.commit()
        flash('Congratulations, you created a new chat!')
        return redirect(url_for('chat_id',id=chat.id))
    return render_template('create_new_chat.html',title='Create new chat', form=form)

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


@app.route('/voice', methods=['POST'])
def voice_rec():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said : {}".format(text))
        except:
            print("Sorry could not recognize what you said")
    return text


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
