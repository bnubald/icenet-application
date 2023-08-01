from flask import jsonify

def get_version():
    return jsonify("0.1.0")
