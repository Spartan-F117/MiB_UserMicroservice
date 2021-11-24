import json
from mib.db_model.user_db import User
import jsonify

def check_none(**kwargs):
    for name, arg in zip(kwargs.keys(), kwargs.values()):
        if arg is None:
            raise ValueError('You can\'t set %s argument to None' % name)


def login(payload):
    print("userMicroservice - login function ")
    print("User:"+payload["email"])
    print("password:" + payload["password"])

    check_none(email=payload['email'])
    user_q = User.query.filter(User.email == payload['email']).first()

    # create response template
    response = {
        'authentication': 'failure',
        'user': None
    }
    response_code = 201

    #if the password of the user is correct
    if user_q and user_q.authenticate(payload['password']):
        response['authentication'] = 'success'
        response['user'] = user_q.serialize()
        response_code = 200

    return jsonify(response), response_code


def logout():
    return json.dumps({"body":"logout"})