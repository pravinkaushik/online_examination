from flask import Flask, jsonify, request
from flask_jwt_extended import (
     get_jwt_claims, JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, fresh_jwt_required
)
from flask import Blueprint
from service import user_management_service
from service import exam_config_management_service
from model.user import User
import requests
import json
import random
import string
user_management_api = Blueprint('user_management_api', __name__)

# This is an example of a complex object that we could build
# a JWT from. In practice, this will likely be something
# like a SQLAlchemy instance.
class UserObject:
    def __init__(self, id, email, roles):
        self.id = id
        self.email = email
        self.roles = roles

# exam_config API
@user_management_api.route("/validate_login", methods = ['GET'])
@jwt_required
def validate_login():
    return jsonify("001"), 200


@user_management_api.route("/home")
@jwt_required
def home():
    ret = {
        'current_identity': get_jwt_identity(),  # test
        'current_id': get_jwt_claims()['id'],
        'current_roles': get_jwt_claims()['roles']  # ['foo', 'bar']
    }
    return jsonify(ret), 200

@user_management_api.route("/")
@jwt_required
def accountList():
    ret = {
        'current_identity': get_jwt_identity(),  # test
        'current_id': get_jwt_claims()['id'],
        'current_roles': get_jwt_claims()['roles']  # ['foo', 'bar']
    }
    return jsonify(ret), 200

@user_management_api.route('/login_exam', methods=['POST'])
def login_exam():
    print("===============")
    exam_config_id = request.json.get('exam_config_id', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    print("===============" + exam_config_id  + email + password)
    candidate = exam_config_management_service.candidate_login(email, exam_config_id, password)
    if candidate is None:
        print("candidate.id")
        return jsonify({"msg": "Bad username or password"}), 401
    print(candidate.id)
    # Create an example UserObject
    user = UserObject(id=candidate.id, email=candidate.email, roles=['candidate'])

    # We can now pass this complex object directly to the
    # create_access_token method. This will allow us to access
    # the properties of this object in the user_claims_loader
    # function, and get the identity of this object from the
    # user_identity_loader function.

    ret = {
        'access_token': create_access_token(identity=user, fresh=True),
        'refresh_token': create_refresh_token(identity=user),
        'current_identity': email,
        'role': 'candidate'
    }
    print(ret)
    return jsonify(ret), 200


@user_management_api.route('/login', methods=['POST'])
def login():
    print("===============")
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    print("===============" + email + password)
    user = user_management_service.validate_user(email, password)
    if user is None:
        print("user.id")
        return jsonify({"msg": "Bad username or password"}), 401
    print(user.id)
    # Create an example UserObject
    user = UserObject(id=user.id, email=user.email, roles=['exam_owner'])

    # We can now pass this complex object directly to the
    # create_access_token method. This will allow us to access
    # the properties of this object in the user_claims_loader
    # function, and get the identity of this object from the
    # user_identity_loader function.

    ret = {
        'access_token': create_access_token(identity=user, fresh=True),
        'refresh_token': create_refresh_token(identity=user),
        'current_identity': email,
        'role': 'exam_owner'
    }
    print(ret)
    return jsonify(ret), 200


@user_management_api.route('/signup_social_media', methods=['POST'])
def signup_social_media():
    provider = request.json.get('provider', None)
    auth_token = request.json.get('auth_token', None)
    email = isValidSocialToken(auth_token, provider)

    UserObj = user_management_service.validate_user_email(email)
    if UserObj is None:
        UserObj = User(0, email, randomString(), "", 1, 1)
        user_management_service.create_user(UserObj)
        UserObj = user_management_service.validate_user_email(email)

    # Create an example UserObject
    user = UserObject(id=UserObj.id, email=UserObj.email, roles=['exam_owner'])

    ret = {
        'access_token': create_access_token(identity=user, fresh=True),
        'refresh_token': create_refresh_token(identity=user),
        'current_identity': email,
        'role': 'exam_owner'
    }
    print(ret)
    return jsonify(ret), 200


@user_management_api.route('/signup', methods=['POST'])
def signup():
    print("===============")

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    print("===============" + email + password )


    ret = {
        'message': "Activation linkhas been send to Your Email."
    }
    print(ret)
    return jsonify(ret), 200


# Refresh token endpoint. This will generate a new access token from
# the refresh token, but will mark that access token as non-fresh,
# as we do not actually verify a password in this endpoint.
@user_management_api.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    ret = {'access_token': new_token}
    return jsonify(ret), 200


# Fresh login endpoint. This is designed to be used if we need to
# make a fresh token for a user (by verifying they have the
# correct username and password). Unlike the standard login endpoint,
# this will only return a new access token, so that we don't keep
# generating new refresh tokens, which entirely defeats their point.
@user_management_api.route('/fresh-login', methods=['POST'])
def fresh_login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = user_management_service.validate_user(email, password)
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401

    # Create an example UserObject
    user = UserObject(id=user.id, email=user.email, roles=['exam_owner'])

    new_token = create_access_token(identity=user, fresh=True)
    ret = {'access_token': new_token}
    return jsonify(ret), 200

# Only fresh JWTs can access this endpoint
@user_management_api.route('/protected-fresh', methods=['GET'])
@fresh_jwt_required
def protected_fresh():
    username = get_jwt_identity()
    return jsonify(fresh_logged_in_as=username), 200

@user_management_api.route('/protected', methods=['GET'])
@jwt_required
def protected():
    ret = {
        'current_identity': get_jwt_identity(),  # test
        'current_id': get_jwt_claims()['id'],
        'current_roles': get_jwt_claims()['roles']  # ['foo', 'bar']
    }
    return jsonify(ret), 200


def isValidSocialToken(token, provider):
    if(provider == "FB"):
        API_ENDPOINT = "https://graph.facebook.com/me?fields=email,name&access_token="+token
        r = requests.get(url = API_ENDPOINT)
        data = json.loads(r.text)
        email = data.get("email",None)
        return email
    else:
        API_ENDPOINT = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="+token
        r = requests.get(url = API_ENDPOINT)
        data = json.loads(r.text)
        email = data.get("email",None)
        return email


def randomString(stringLength=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))