import json
from mib.db_model.user_db import User, Filter_list
from flask import jsonify, request
import datetime
from datetime import datetime
from mib import db
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash

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
        print(response['user'])
        response_code = 200
        print("authenticate ok")

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


def profile_filter(user_id: int):

    post_data = request.get_json()

    user_filter_list = db.session.query(Filter_list).filter(Filter_list.user_id==user_id)
    response = {
        'response': 'info sent',
        'filter': ''
    }
    if user_filter_list.first() is not None:
        response['filter'] = user_filter_list.first().list
    return jsonify(response), 201


def change_filter():

    post_data = request.get_json()

    print("change filter branch")
    new_filter = Filter_list()
    new_filter.list = post_data.get('filter')
    new_filter.user_id = post_data.get('user_id')
    user_filter_list = db.session.query(Filter_list).filter(Filter_list.user_id==post_data.get('user_id'))
    if user_filter_list.first() is not None:
        db.session.query(Filter_list).filter(Filter_list.user_id==post_data.get('user_id')).delete()
        db.session.add(new_filter)
    else:
        db.session.add(new_filter)
    db.session.commit()
    response = {
        'response': 'filter updated',
        'filter': post_data.get('filter')
    }
    return jsonify(response), 203


def change_info():

    post_data = request.get_json()

    print("change info branch")
    user_q = User.query.filter(User.id == post_data.get('user_id')).first()
    if check_password_hash(user_q.password, post_data.get('old_password')) : #check if the password that is put in the form is corrected
        user_to_modify = db.session.query(User).filter(User.id==post_data.get('user_id')).first()
        if post_data.get('firstname') is not '':
            user_to_modify.firstname = post_data.get('firstname')
        if post_data.get('surname') is not '':
            user_to_modify.lastname = post_data.get('surname')
        if post_data.get('birthday') is not '':
            user_to_modify.date_of_birth = datetime.fromisoformat(post_data.get('birthday'))
        if post_data.get('location') is not '':
            user_to_modify.location = post_data.get('location')
        if post_data.get('new_password') is not '':
            user_to_modify.password = generate_password_hash(post_data.get('new_password'))
        db.session.commit()
        print("info changed")
        user_filter_list = db.session.query(Filter_list).filter(Filter_list.user_id==post_data.get('user_id'))
        if user_filter_list.first() is not None:
            response = {
                'response': 'info changed',
                'filter': user_filter_list.first().list
            }
        else:
            response = {
                'response': 'info changed',
                'filter': ''
            }
        return jsonify(response), 201
    else:
        print("old password incorrect")
        user_filter_list = db.session.query(Filter_list).filter(Filter_list.user_id==post_data.get('user_id'))
        if user_filter_list.first() is not None:
            response = {
                'response': 'info not changed',
                'filter': user_filter_list.first().list
            }
        else:
            response = {
                'response': 'info not changed',
                'filter': ''
            }
        return jsonify(response), 202






