from flask import Flask, request
from datetime import datetime
import json

app = Flask(__name__)
number_of_planes = 5
plane_speed = 10
darkness = False

@app.route("/info")
def hello_world():
    global number_of_planes, plane_speed, darkness
    return json.dumps({"number_of_planes": number_of_planes, "plane_speed": plane_speed, "darkness": False})

@app.route("/post_pulse_data", methods=['POST'])
def get_post():
    data = request.data
    string_data = json.loads(data)
    now = datetime.now()
    string_data["date"] = now.strftime("%d-%m-%Y (%H:%M:%S.%f)")
    with open("data/data.json", "a+") as f:
        f.write(json.dumps(string_data))
        f.write("\n")
    return ""
