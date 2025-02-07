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


# @app.route('/users', methods=['POST'])
# def users() -> str:
#     """Register a new user
#     """
#     email = request.form.get('email')
#     password = request.form.get('password')
#     # if not email or password:
#     # #return jsonify({"message": "Email and password required"}), 400

#     try:
#         user = AUTH.register_user(email, password)
#         return jsonify({"email": user.email, "message": "User created"}), 201
#     except Exception:
#         return jsonify({"message": "email already registered"}), 400
@app.route('/users', methods=['POST'])
def users() -> str:
    """_summary_
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # regsiter user if user does not exist
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not (AUTH.valid_login(email, password)):
        abort(401)
    else:
        # create a new session
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """_summary_
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def Profile() -> str:
    """_summary_
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": email, "reset_token": reset_token}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
