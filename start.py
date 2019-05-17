from app import app, socketio


#==========================================#
'''
Get local host IP for setting up socket for chat.
'''
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
host = s.getsockname()[0]
s.close()
#==========================================#


socketio.run(app, host=host)
