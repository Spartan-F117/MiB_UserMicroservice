from flask import jsonify
from mib.resource.user_manager import UserManager
from mib.db_model.user_db import db, User



def get_user(user_id):
    """
    Get a user by its current id.
    :param user_id: user it
    :return: json response
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200

def increment_point_user(user_id):
    """
    Get a user by its current id and increment lottery point of the user
    :param user_id: user it
    :return: json response
    """
    # user_winner = db.session.query(User).filter(User.id == user_id)
    # user_winner.first().lottery_points += 1
    # db.session.commit()

    user = UserManager.retrieve_by_id(user_id)
    user.lottery_points += 1
    db.session.commit()

    user2 = UserManager.retrieve_by_id(user_id)
    print("punti lotteria dell'utente vincitore:")
    print(user2.lottery_points)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200


def get_user_by_email(user_email):
    """
    Get a user by its current email.
    :param user_email: user email
    :return: json response
    """
    user = UserManager.retrieve_by_email(user_email)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200

def get_user_by_nickname(user_nickname):
    
    user = UserManager.retrieve_by_nickname(user_nickname)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200


def delete_user(user_id):
    """
    Delete the user with id = user_id.
    :param user_id the id of user to be deleted
    :return json response
    """
    UserManager.delete_user_by_id(user_id)
    response_object = {
        'status': 'success',
        'message': 'Successfully deleted',
    }

    return jsonify(response_object), 202