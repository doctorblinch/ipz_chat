from app import db
from datetime import datetime
#from models import User
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

#   chat = db.relationship('Chat')
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"))

    def __repr__(self):
        return 'User {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

#    users = db.relationship("User", backref="chat", lazy='dynamic')
    users = db.relationship("User")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), default='global_chat')

    def __repr__(self):
        return '<Message: {}, from: {}, to: {}>'.format(self.body, self.user_id, self.chat_id)
        #return self.body


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


def get_previous_messages(quantity=15, chat_id='global_chat'):
    #messages_for_sending = Message.query.limit(quantity).all()
    messages_for_sending =  Message.query.filter_by(chat_id=chat_id).order_by(Message.id.desc()).limit(quantity).all()
    return messages_for_sending
