
from flask import Blueprint, request
from flask_api import FlaskAPI

api = Blueprint('api_v1', __name__, url_prefix='/api/v1')

@api.route("/chain", methods=["GET", "POST"])
def chain():
    if request.method == "GET":
        pass

    elif request.method == "POST":
        pass

    return "unko"
