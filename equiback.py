from flask import Flask, request, jsonify
from engine import *
import base64
import json
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HobjShtfaLthqyFF35w1UwKhfz6IceeY6XpmF6a0fovNYmPBXE+QpWiFiGNOVwfoaWWmsknSGlPHywctskkKXQ=='


@app.route('/success/', methods=["GET","POST"])
def success():
    if request.method == "POST":
        data = request.get_json()
        startTime = time.time()
        result = equishellEngine(data["message"])
        resp = base64.b64encode(str.encode(json.dumps({"answer": result, "time": (startTime-time.time())}))).decode("utf-8")
        return resp
        # return jsonify({"data": resp})
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9013,threaded = True)