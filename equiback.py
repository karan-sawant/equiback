from flask_socketio import SocketIO, send, emit
from flask import Flask
from engine import *
import base64
import json
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HobjShtfaLthqyFF35w1UwKhfz6IceeY6XpmF6a0fovNYmPBXE+QpWiFiGNOVwfoaWWmsknSGlPHywctskkKXQ=='


socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(data):
    startTime = time.time()
    result = equishellEngine(data["message"])
    resp = base64.b64encode(str.encode(json.dumps({"answer": result, "time": (startTime-time.time())}))).decode("utf-8")
    emit("answers", resp)
if __name__ == '__main__':
    socketio.run(app, debug=False, host="127.0.0.1", port="9020")