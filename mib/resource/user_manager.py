from mib.db_model.user_db import User
from mib import db

class Manager(object):

    db_session = db.session

    @staticmethod
    def check_none(**kwargs):
        for name, arg in zip(kwargs.keys(), kwargs.values()):
            if arg is None:
                raise ValueError('You can\'t set %s argument to None' % name)

    @staticmethod
    def create(**kwargs):
        Manager.check_none(**kwargs)

        for bean in kwargs.values():
            db.session.add(bean)

        db.session.commit()

    @staticmethod
    def retrieve():
        """
        It should implemented by child
        :return:
        """
        pass

    @staticmethod
    def update(**kwargs):
        Manager.check_none(**kwargs)
        db.session.commit()

    @staticmethod
    def delete(**kwargs):
        Manager.check_none(**kwargs)

        for bean in kwargs.values():
            db.session.delete(bean)
        db.session.commit()

class UserManager(Manager):

    @staticmethod
    def create_user(user: User):
        Manager.create(user=user)

    @staticmethod
    def retrieve_by_id(id_):
        #Manager.check_none(id=id_)
        #return User.query.get(id_)
        return db.session.query(User).filter(User.id==id_).first()

    @staticmethod
    def retrieve_by_email(email):
        Manager.check_none(email=email)
        return User.query.filter(User.email == email).first()

    @staticmethod
    def retrieve_by_phone(phone):
        Manager.check_none(phone=phone)
        return User.query.filter(User.phone == phone).first()

    @staticmethod
    def update_user(user: User):
        Manager.update(user=user)

    @staticmethod
    def delete_user(user: User):
        Manager.delete(user=user)

    @staticmethod
    def delete_user_by_id(id_: int):
        user = UserManager.retrieve_by_id(id_)
        UserManager.delete_user(user)