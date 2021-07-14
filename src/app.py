from flask import Flask, request
from datetime import datetime
import json

app = Flask(__name__)
i = 0

@app.route("/")
def hello_world():
    global i
    i += 1
    return json.dumps({"data": str(i)})

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
