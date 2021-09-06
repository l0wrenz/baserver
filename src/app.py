from flask import Flask, request, render_template, redirect, url_for, send_file
import heartpy as hp
from datetime import datetime
import json
import sys
import os
import io

app = Flask(__name__)
number_of_planes = 5
plane_speed = 10
darkness = False
id = 0


@app.route('/get_image')
def get_image():
    return send_file("heart_plot.jpg", mimetype='image/jpeg')


@app.route("/info")
def hello_world():
    global number_of_planes, plane_speed, darkness
    return json.dumps({"number_of_planes": number_of_planes, "plane_speed": plane_speed, "darkness": darkness})


@app.route("/settings")
def settings():
    global number_of_planes, plane_speed, darkness
    return render_template("index.html", number_of_planes=number_of_planes, plane_speed=plane_speed, darkness=darkness)


@app.route("/handle_form", methods=["POST"])
def handle_form():
    global number_of_planes, plane_speed, darkness
    data = request.form

    number_of_planes = int(data["number_of_planes"])
    plane_speed = int(data["plane_speed"])
    darkness = data["darkness"]
    print(darkness, file=sys.stderr)
    if darkness == "1":
        darkness = True
    else:
        darkness = False

    print(darkness, file=sys.stderr)
    return redirect(url_for("settings"))


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

    req_data = request.data
    data_dict = json.loads(req_data)

    now = datetime.now()
    data_dict["date"] = now.strftime("%d-%m-%Y (%H:%M:%S.%f)")
    data_dict["id"] = id
    path = f"data/pulse_data_id_{str(id)}.json"
    startupCheck(path)

    with open(path, "r+") as f:
        try:
            json_decoded = json.load(f)
            print(json_decoded, file=sys.stderr)
            json_decoded.append(data_dict.copy())
            print(json_decoded, file=sys.stderr)

            with open(path, 'w') as outfile:
                json.dump(json_decoded, outfile, indent=4)
                # sort_keys, indent are optional and used for pretty-write
        except Exception as e:
            print(e, file=sys.stderr)

    data = data_dict["data"]["new_arr"]
    timediff = data_dict["data"]["timediff"]
    working_data, measures = hp.process(
        data, hp.get_samplerate_mstimer(timediff))
    plot_object = hp.plotter(working_data, measures, show=False)

    plot_object.savefig('heart_plot.jpg')

    return ""


@app.route("/post_score", methods=['POST'])
def post_game_data():

    global id, number_of_planes, plane_speed, darkness

    req_data = request.form
    print(req_data)
    data_dict = {}

    now = datetime.now()
    data_dict["date"] = now.strftime("%d-%m-%Y (%H:%M:%S.%f)")
    data_dict["crashes"] = req_data["crashes"]
    data_dict["wrong_airport_score"] = req_data["wrong_airport_score"]
    data_dict["correct"] = req_data["correct"]
    data_dict["number_of_planes"] = number_of_planes
    data_dict["plane_speed"] = plane_speed
    data_dict["darkness"] = darkness

    path = f"data/game_data_id_{str(id)}.json"
    startupCheck(path)

    with open(path, "r+") as f:
        try:
            json_decoded = json.load(f)
            print(json_decoded, file=sys.stderr)
            json_decoded.append(data_dict.copy())
            print(json_decoded, file=sys.stderr)

            with open(path, 'w') as outfile:
                json.dump(json_decoded, outfile, indent=4)
                # sort_keys, indent are optional and used for pretty-write
        except Exception as e:
            print(e, file=sys.stderr)
    return ""


def startupCheck(path):
    if os.path.isfile(path) and os.access(path, os.R_OK):
        # checks if file exists
        print("File exists and is readable", file=sys.stderr)
    else:
        print(
            "Either file is missing or is not readable, creating file...", file=sys.stderr)
        with io.open(path, 'w') as db_file:
            db_file.write(json.dumps([]))
