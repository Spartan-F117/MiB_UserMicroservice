import json
from mib.db_model.user_db import User
from flask import jsonify, request
import datetime
from datetime import datetime
from mib import db


def check_none(**kwargs):
    for name, arg in zip(kwargs.keys(), kwargs.values()):
        if arg is None:
            raise ValueError('You can\'t set %s argument to None' % name)


def validate_date(date_text):
    try:
        print(date_text)
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


def login(payload):
    print("userMicroservice - login function ")
    print("User:"+payload["email"])

    check_none(email=payload['email'])
    user_q = User.query.filter(User.email == str(payload['email'])).first()

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


def create_user():
    print("userMicroservice - create_user function ")

    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')
    nickname = post_data.get('nickname')
    location = post_data.get('location')
    date_of_birth = post_data.get('date_of_birth')
    firstname = post_data.get('firstname')
    lastname = post_data.get('lastname')

    response = {
        'response': 'already register',
        'user': None
    }

    # check if email exist
    email_exist_control = User.query.filter(User.email == email).first()
    if email_exist_control is not None:  # check if the email exists
        print("email is already registered!")
        return jsonify(response), 202

    # check if nickname exist
    nick_exist_control = User.query.filter(User.nickname == nickname)
    if nick_exist_control.first() is not None:  # check if the nickname exists
        print("This nickname is not available!")
        return jsonify(response), 202

    # check if date is valid (valid format and not in a future date)
    if not validate_date(date_of_birth):
        print("Invalid data format")
        response["response"] ="invalid date format"
        return jsonify(response), 202

    birthday = datetime.strptime(date_of_birth, '%Y-%m-%d')

    if birthday >= datetime.today():
        print("Invalid data - born in the future")
        response["response"] = "born in the future"
        return jsonify(response), 202

    user = User()
    user.set_email(email)
    user.set_password(password)
    user.set_firstname(firstname)
    user.set_lastname(lastname)
    user.set_birthday(birthday)
    user.set_location(location)
    user.set_nickname(nickname)

    # Add user to the db
    db.session.add(user)
    db.session.commit()

    response["response"] = "user created"
    response["user"] = user.serialize()

    return jsonify(response), 201


def show_users():
    post_data = request.get_json()
    id_user = post_data.get('id')
    _users = db.session.query(User).filter(User.is_deleted == False).filter(User.id != id_user)
    response = {
        'list_users': _users
    }
    return jsonify(response), 201