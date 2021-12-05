from re import T, U
import unittest

from faker import Faker

from model_test import ModelTest


class TestUser(ModelTest):

    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestUser, cls).setUpClass()

        from mib.db_model import User
        cls.user = User

    @staticmethod
    def assertUserEquals(value, expected):
        t = unittest.FunctionTestCase(TestUser)
        t.assertEqual(value.email, expected.email)
        t.assertEqual(value.password, expected.password)
        t.assertEqual(value.is_active, expected.is_active)
        t.assertEqual(value.authenticated, False)
        t.assertEqual(value.is_anonymous, expected.is_anonymous)

    @staticmethod
    def generate_random_user():
        email = TestUser.faker.email()
        password = TestUser.faker.password()
        is_active = TestUser.faker.boolean()
        is_admin = TestUser.faker.boolean()
        authenticated = TestUser.faker.boolean()
        is_anonymous = TestUser.faker.boolean()
        first_name = TestUser.faker.first_name()
        last_name = TestUser.faker.last_name()
        phone = TestUser.faker.phone_number()

        from mib.db_model import User

        user = User(
            email=email,
            password=password,
            is_active=is_active,
            is_admin=is_admin,
            authenticated=authenticated,
            is_anonymous=is_anonymous,
            firstname=first_name,
            lastname=last_name,
            nickname='nick'
        )

        return user

    def test_set_password(self):
        user = TestUser.generate_random_user()
        password = self.faker.password(length=10, special_chars=False, upper_case=False)
        user.set_password(password)

        self.assertEqual(
            user.authenticate(password),
            True
        )
    
    def test_set_email(self):
        user = TestUser.generate_random_user()
        email = self.faker.email()
        user.set_email(email)
        self.assertEqual(email, user.email)

    def test_set_firstname(self):
        user = TestUser.generate_random_user()
        firstname = self.faker.first_name()
        user.set_firstname(firstname)
        self.assertEqual(firstname, user.firstname)

    def test_set_lastname(self):
        user = TestUser.generate_random_user()
        lastname = self.faker.last_name()
        user.set_lastname(lastname)
        self.assertEqual(lastname, user.lastname)

    def test_set_nickname(self):
        user = TestUser.generate_random_user()
        nickname = self.faker.first_name()
        user.set_nickname(nickname)
        self.assertEqual(nickname, user.nickname)