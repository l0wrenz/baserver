from flask import Flask, request
from datetime import datetime
import json
import sys

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
def post_pulse_data():

    global id

    request_data = request.data
    print(request_data)
    data_dict = json.loads(request_data)
    now = datetime.now()
    data_dict["date"] = now.strftime("%d-%m-%Y (%H:%M:%S.%f)")
    data_dict["id"] = id
    data = []
    
    with open(f"data/game_data{str(id)}.json", "w") as f:
        print("sad")

    with open(f"data/pulse_data{str(id)}.json", "r") as f:
        raw_data = f.read()
        if raw_data: data.append(json.loads(raw_data))

    with open(f"data/pulse_data{str(id)}.json", "a+") as f:
        f.write(json.dumps(data.append(data_dict)))

    return ""


@app.route("/post_game_data", methods=['POST'])
def post_game_data():
    
    global id

    req_data = request.data
    data_dict = json.loads(req_data)
    print(data_dict, file=sys.stderr)

    now = datetime.now()
    data_dict["date"] = now.strftime("%d-%m-%Y (%H:%M:%S.%f)")
    data_dict["id"] = id
    data = []
    
    with open(f"data/game_data{str(id)}.json", "w+") as f:
        print("sad")

    with open(f"data/game_data{str(id)}.json", "r+") as f:
        try:
            raw_data = f.read()
            json_decoded = json.loads(raw_data)
            old_data = json_decoded
            data = old_data + data
            print(data, file=sys.stderr)

        except Exception as e:
            print(e, file=sys.stderr)
    return ""