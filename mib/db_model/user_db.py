from werkzeug.security import generate_password_hash, check_password_hash
from mib import db

class User(db.Model):
    __tablename__ = 'User'

    # A list of fields to be serialized
    SERIALIZE_LIST = ['id', 'email', 'is_active', 'authenticated', 'is_anonymous']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    # Create unique id for the user
    email = db.Column(db.Unicode(128), nullable=False)                  # Create email for the user
    firstname = db.Column(db.Unicode(128))                              # Firstname of user
    lastname = db.Column(db.Unicode(128))                               # Surname of user
    password = db.Column(db.Unicode(128))                               # Create password for user
    date_of_birth = db.Column(db.Date)                                  # Users date of birth
    location = db.Column(db.Unicode(128))                               # Users location
    nickname = db.Column(db.Unicode(128))                               # Nickname of the user
    is_active = db.Column(db.Boolean, default=False)                    # Checks active status of user (Online/Offline)
    is_admin = db.Column(db.Boolean, default=False)                     # Checks if user is admin or not (True if admin)
    is_deleted = db.Column(db.Boolean, default=False)                   # Checks that the user is deleted or not (True if deleted)
    is_anonymous = False                                                # Checks if user is logged in or not
    authenticated = db.Column(db.Boolean, default=True)
    lottery_points = db.Column(db.Integer, default = 0)                 # point winned partecipating to the monthly lottery

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    # set the user password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def set_birthday(self, date_of_birth):
        self.date_of_birth = date_of_birth

    def set_location(self, location):
        self.location = location

    def set_email(self, email):
        self.email = email

    def set_firstname(self, firstname):
        self.firstname = firstname

    def set_lastname(self, lastname):
        self.lastname = lastname

    def set_nickname(self,nickname):
        self.nickname = nickname


    @property
    def is_authenticated(self):
        return self.authenticated

    # return true is the user is authenticated
    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self.authenticated = checked
        self.is_active = checked
        return self.authenticated

    # Return the user id
    def get_id(self):
        return self.id

    def serialize(self):
        return dict([(k, self.__getattribute__(k)) for k in self.SERIALIZE_LIST])

class Filter_list(db.Model):
    __tablename__ = 'filter'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    list = db.Column(db.Unicode(128), nullable=True)
