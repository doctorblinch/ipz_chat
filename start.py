from app import app, socketio

#app.run(host= '192.168.0.105')
socketio.run(app, host='192.168.0.101')
