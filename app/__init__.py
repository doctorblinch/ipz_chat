from flask import Flask
from config import Config
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
socketio = SocketIO(app)

from app import routes, models


# add Admin
from app.models import *
from app.admin_view import *

admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(RecordAdminView(Message, db.session))
admin.add_view(UserAdminView(Chat, db.session))
