#from services import root_dir, nice_json
from flask import Flask
from werkzeug.exceptions import NotFound, ServiceUnavailable
import json
import requests

import os
from flask import make_response


def root_dir():
    """ Returns root director for this project """
    return os.path.dirname(os.path.realpath(__file__ + '/..'))


def nice_json(arg):
    print("Hello")
    response = make_response(json.dumps(arg, sort_keys = True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response
app = Flask(__name__)

with open("users.json", "r") as f:
    users = json.load(f)

print(users)

@app.route("/", methods=['GET'])
def hello():
    return """Welcome to e-commerce site.\n
        Hit these url's to get specific info\n
        users: /users,\n
        user: /users/<username>,\n
        bookings: /users/<username>/product_booking,"""


@app.route("/users", methods=['GET'])
def users_list():
    return nice_json(users)


@app.route("/users/<username>", methods=['GET'])
def user_record(username):
    if username not in users:
        raise NotFound

    return "Welcome {} . ".format(users[username]['name'])


@app.route("/users/<username>/product_booking", methods=['GET'])
def user_bookings(username):
    """
    Gets product booking information from the 'Bookings Service' for the user, and
     product ratings etc. from the 'product Service' and returns a list.
    :param username:
    :return: List of Users bookings
    """
    if username not in users:
        raise NotFound("User '{}' not found.".format(username))

    try:
        users_bookings = requests.get("http://test2_booking:81/product_booking/{}".format(username))
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailable("The Bookings service is unavailable.")

    if users_bookings.status_code == 404:
        raise NotFound("No bookings were found for {}".format(username))

    users_bookings = users_bookings.json()
    print(users_bookings)

    #For each booking, get the rating and the product info
    result = {}
    for date, products in users_bookings.items():
        result[date] = []
        for productid in products:
            try:
                products_resp = requests.get("http://test1_product:82/products/{}".format(productid))
            except requests.exceptions.ConnectionError:
                raise ServiceUnavailable("The Product service is unavailable.")
            products_resp = products_resp.json()
            print(products_resp)
            result[date].append({
                "type": products_resp["type"],
                "rating": products_resp["rating"],
                "gender": products_resp["gender"]
            })

    return nice_json(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
