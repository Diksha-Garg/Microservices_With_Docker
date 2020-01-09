from flask import Flask
import json
import os
from flask import make_response
from werkzeug.exceptions import NotFound

def root_dir():
    """ Returns root director for this project """
    return os.path.dirname(os.path.realpath(__file__ + '/..'))
def nice_json(arg):
    response = make_response(json.dumps(arg, sort_keys = True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response
app = Flask(__name__)

with open("bookings.json", "r") as f:
    bookings = json.load(f)

@app.route("/", methods=['GET'])
def hello():
    return "Welcome to booking service"

@app.route("/product_booking", methods=['GET'])
def booking_list():
    return nice_json(bookings)


@app.route("/product_booking/<username>", methods=['GET'])
def booking_record(username):
    if username not in bookings:
        raise NotFound

    return nice_json(bookings[username])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
