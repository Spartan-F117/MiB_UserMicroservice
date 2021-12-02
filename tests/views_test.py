import unittest


class ViewTest(unittest.TestCase):
    """
    This class should be implemented by
    all classes that tests resources
    """
    client = None

    @classmethod
    def setUpClass(self):
        from mib import create_app
        app = create_app()
        self.client = app.test_client()

    def test_create_user(self):
    
        print('trying creating user....')

        payload = dict(email='bob@example.com', 
                    password='pass123', date_of_birth='01/01/1999', 
                    firstname='Bob', lastname='Johnson', 
                    nickname='Bobby', location='Pisa')
        
        response = self.client.post("/create_user", json=payload)
        
        assert response.status_code == 202

    def test_login(self):

        print('trying login....')

        payload = dict(email='bob@example.com', password='pass123')
        response = self.client.post("/authenticate", json=payload)
        assert response.status_code == 201

    def test_logout(self):

        print('trying logout....')

        response = self.client.post("/logout/bob@example.com")
        assert response.status_code == 200

    def test_show_user(self):

        print('trying show user....')

        payload = dict(id='2')
        response = self.client.post("/show_users", json=payload)
        assert response.status_code == 201

    def test_add_blacklist(self):

        print('trying add blacklist....')

        payload = dict(id_owner='2', id_to_insert='5')
        response = self.client.post("/blacklist", json=payload)
        json_response = response.json

        if json_response["message"] == 'blacklist add':
            assert response.status_code == 202
        else:
            assert response.status_code == 303

    def test_blacklist_info(self):

        print('trying blacklist info....')

        response = self.client.post("/blacklist/2/5")
        assert response.status_code == 202

    def test_delete_blacklist(self):

        print('trying delete blacklist....')

        payload = dict(id_owner='2', id_to_insert='5')
        response = self.client.post("/delete_blacklist", json=payload)
        json_response = response.json

        if json_response["message"] == 'user removed correctly':
            assert response.status_code == 202
        else:
            assert response.status_code == 303

    def test_report_list(self):

        print('trying report list....')

        payload = dict(id_owner='3', id_to_insert='2')
        response = self.client.post("/reportlist", json=payload)
        json_response = response.json

        if json_response["message"] == 'added to reportlist':
            assert response.status_code == 202
        else:
            assert response.status_code == 303

    def test_profile_filter(self):

        print('trying profile filter....')

        response = self.client.post("/profile_filter/2")
        assert response.status_code == 201

    def test_change_filter(self):

        print('trying change filter....')

        payload = dict(filter='', user_id='2')
        response = self.client.post("/change_filter", json=payload)
        assert response.status_code == 203

    def test_change_info(self):

        print('trying change info....')

        payload = dict(user_id='2', firstname='first_name', lastname='last_name',
                    date_of_birth='02/02/1998', new_password='pass0000',
                    old_password='pass123', location='Livorno')
        response = self.client.post("/change_info", json=payload)
        assert response.status_code == 202

    def test_delete_user(self):

        print('trying delete user....')

        payload = dict(user_id='2')
        response = self.client.post("/delete_user", json=payload)
        json_response = response.json

        if json_response["response"] == 'user deleted':
            assert response.status_code == 201
        else:
            assert response.status_code == 301

    def test_decrease_lottery_points(self):

        print('trying decrease lottery points....')

        response = self.client.post("/decrease_lottery_points/5")
        assert response.status_code == 200
