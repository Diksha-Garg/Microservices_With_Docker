from flask import Flask
from werkzeug.exceptions import NotFound
import os
import json
from flask import make_response


def root_dir():
    """ Returns root director for this project """
    return os.path.dirname(os.path.realpath(__file__ + '/..'))


def nice_json(arg):
    response = make_response(json.dumps(arg, sort_keys = True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response
app = Flask(__name__)

with open("products.json", "r") as f:
    products = json.load(f)

print(products)
@app.route("/", methods=['GET'])
def hello():
    return "Welcome to product services"

@app.route("/products/<productid>", methods=['GET'])
def product_info(productid):
    if productid not in products:
        raise NotFound

    result = products[productid]
    print(result)


    return nice_json(result)


@app.route("/products", methods=['GET'])
def product_record():
    return nice_json(products)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='82')

