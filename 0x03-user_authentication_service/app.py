#!/usr/bin/env python3
"""Flask app
"""


from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> str:
    """ Home Route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """Register a new user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    # if not email or password:
    # #return jsonify({"message": "Email and password required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "User created"}), 201
    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
