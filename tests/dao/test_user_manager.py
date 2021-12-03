from faker import Faker

from dao_test import DaoTest



class TestUserManager(DaoTest):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestUserManager, cls).setUpClass()
        from tests.models.test_user import TestUser
        cls.test_user = TestUser
        from mib.resource import user_manager
        cls.user_manager = user_manager.UserManager
        import mib.resource.util_fun as utile
        cls.user_utile = utile

    def test_crud(self):
        for _ in range(0, 10):
            user = self.test_user.generate_random_user()
            self.user_manager.create_user(user=user)
            user1 = self.user_manager.retrieve_by_id(user.id)
            user.set_password(self.faker.password())
            user.email = self.faker.email()
            self.user_manager.update_user(user=user)
            user2 = self.user_manager.retrieve_by_id(user.id)
            self.user_manager.delete_user(user=user)
            assert user2 is not None and user1 is not None

    def test_retried_by_email(self):
        base_user = self.test_user.generate_random_user()
        self.user_manager.create_user(user=base_user)
        retrieved_user = self.user_manager.retrieve_by_email(base_user.email)
        assert retrieved_user is not None

    def test_util(self):
        self.user_utile.get_user('1')