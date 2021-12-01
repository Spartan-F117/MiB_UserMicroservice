import json
import re
from flask import jsonify, request
import datetime
from datetime import datetime
from flask.wrappers import Response
from werkzeug.security import check_password_hash, generate_password_hash
from mib.db_model.user_db import BlackList, ReportList, User, db, Filter_list

POINT_NECESSARY=12

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
    user_q = User.query.filter(User.email == str(payload['email'])).filter(User.is_deleted == False).first()

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
        user_q.is_active = True
        db.session.commit()
        response_code = 200

    return jsonify(response), response_code


def logout(user_email):

    user_q = User.query.filter(User.email == user_email).first()
    user_q.is_active = False
    db.session.commit()

    return json.dumps({"body":"logout"}),200


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
    user.set_isadmin(False)
    # Add user to the db
    db.session.add(user)
    db.session.commit()

    response["response"] = "user created"
    response["user"] = user.serialize()

    return jsonify(response), 201


def show_users():

    post_data = request.get_json()

    id_user = post_data.get('id')
    _users = User.query.filter(User.is_deleted == False).filter(User.id != id_user).all()

    #JSON vuoto
    listobj = []

    for item in _users:
        listobj.append(item.serialize())

    response = {
        'list_users': listobj
    }
    return jsonify(response), 201

def add_blacklist():

    response = {
        'message': 'already in blacklist'
    }

    post_data = request.get_json()

    new_blackList = BlackList()
    new_blackList.user_id = post_data.get('id_owner')
    new_blackList.blacklisted_user_id = post_data.get('id_to_insert')
    new_blackList.id=1

    print(new_blackList.user_id)
    print(new_blackList.blacklisted_user_id)

    _list = db.session.query(BlackList).filter(BlackList.user_id == post_data.get('id_owner')).filter(
        BlackList.blacklisted_user_id == post_data.get('id_to_insert')).first()
    if _list is not None:  # chek if the tupla (current_user.id,user_to_block.id) is just in the db
        print("blacklist already exist")
        return jsonify(response), 303
    else:
        print("ci arrivo")
        db.session.add(new_blackList)
        print ("non ci arrivo")
        db.session.commit()
        print("blacklist add")
        print(db.session.query(BlackList).filter(BlackList.user_id == post_data.get('id_owner')).filter(
        BlackList.blacklisted_user_id == post_data.get('id_to_insert')).first())
        response["message"] = "blacklist add"
        return jsonify(response), 202

def blacklist_info(sender_id, receiver_id):
    print(sender_id)
    print(receiver_id)
    response = {
        'message': 'blacklist is present'
    }
    result = db.session.query(BlackList).filter(BlackList.user_id == receiver_id).filter(BlackList.blacklisted_user_id == sender_id).first()
    print(result)
    if result is not None:
        return jsonify(response), 200
    else:
        response['message']='blacklist is not present'
        return jsonify(response), 202

def remove_blacklist():

    response = {
        'message': 'not in blacklist'
    }

    post_data = request.get_json()
    owner_id = post_data.get('id_owner')
    id_to_insert_blacklist = post_data.get('id_to_insert')

    new_blackList = BlackList()
    new_blackList.user_id = int(owner_id)
    new_blackList.blacklisted_user_id = int(id_to_insert_blacklist)

    blacklist_id = db.session.query(BlackList).filter(BlackList.user_id == new_blackList.user_id).filter(
        BlackList.blacklisted_user_id == new_blackList.blacklisted_user_id)

    if blacklist_id.first() is not None:  # chek if the tupla (current_user.id,user_to_block.id) is just in the db
        db.session.query(BlackList).filter(BlackList.id == blacklist_id.first().id).delete()
        db.session.commit()
        print("removed from blacklist")
        response["message"] = "user removed correctly"
    else:
        print("operation not allowed: the user is not in the blacklist")
        return jsonify(response), 303

    return jsonify(response), 202


def report_list():

    response = {
        'message': 'already in reportlist'
    }

    post_data = request.get_json()
    owner_id = post_data.get('id_owner')
    id_to_insert_reportlist = post_data.get('id_to_insert')

    new_reportlist = ReportList()

    new_reportlist.user_id = owner_id
    new_reportlist.reportlisted_user_id = id_to_insert_reportlist
    new_reportlist.id=1

    _list = db.session.query(ReportList).filter(ReportList.user_id == new_reportlist.user_id).filter(
        ReportList.reportlisted_user_id == new_reportlist.reportlisted_user_id)
    if _list.first() is not None:  # chek if the tupla (current_user.id,user_to_report.id) is just in the db
        print("user already reported")
        return jsonify(response), 303
    else:
        db.session.add(new_reportlist)
        db.session.commit()
        print("added to reportlist")
        response["message"] = "added to reportlist"
        return jsonify(response), 202


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


def delete_user():
    print("userMicroservice - delete_user function ")

    post_data = request.get_json()

    user_id = post_data.get('user_id')

    response = {
        'response': 'user not deleted'
    }

    response_code = 301

    user_logged = User.query.filter(User.id == user_id).first()
    user_logged.is_deleted = True
    db.session.commit()

    if user_logged.is_deleted == True:
        response_code = 201
        response["response"] = "user deleted"

    return jsonify(response), response_code

def decrease_lottery_points(user_id):
    user = User.query.filter(User.id == user_id).first()
    user.lottery_points -= POINT_NECESSARY
    db.session.commit()
    return 200
    



