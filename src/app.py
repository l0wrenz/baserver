from flask import Flask, request
from datetime import datetime
import json


app = Flask(__name__)
number_of_planes = 5
plane_speed = 10
darkness = False
id = 0

@app.route("/info")
def hello_world():
    global number_of_planes, plane_speed, darkness
    return json.dumps({"number_of_planes": number_of_planes, "plane_speed": plane_speed, "darkness": darkness})

@app.route("/switch_difficulty", methods=['POST'])
def switch_difficulty():
    global number_of_planes, plane_speed, darkness
    data = request.data
    data_dict = json.loads(data)

    number_of_planes = data_dict["number_of_planes"]
    plane_speed = data_dict["plane_speed"]
    darkness = data_dict["darkness"]

    return ""

@app.route("/switch_id", methods=['POST'])
def switch_id():
    global id
    data = request.data
    data_dict = json.loads(data)
    id = data_dict["id"]
    return ""

@app.route("/post_pulse_data", methods=['POST'])
def get_post():

    global id

    data = request.data
    string_data = json.loads(data)
    now = datetime.now()
    string_data["date"] = now.strftime("%d-%m-%Y (%H:%M:%S.%f)")
    string_data["id"] = id

    with open(f"data/pulse_data{id}.json", "a+") as f:
        f.write(json.dumps(string_data))
        f.write("\n")
    return ""


@app.route("/post_game_data", methods=['POST'])
def get_post():
    
    global id

    data = request.data
    data_dict = json.loads(data)

    now = datetime.now()
    data_dict["date"] = now.strftime("%d-%m-%Y (%H:%M:%S.%f)")
    data_dict["id"] = id
    data = []

    with open(f"data/game_data{str(id)}.json", "r+") as f:
        data.append(json.loads(f))

    with open(f"data/game_data{str(id)}.json", "a+") as f:
        f.write(json.dumps(data.append(data_dict)))

    return ""