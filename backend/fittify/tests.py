from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserCreationTests(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "Simple1234"
        self.email = "testuser@example.com"
        self.first_name = "1"
        self.last_name = "2"
        self.token = ""
        self.id = 1

    def test_user_creation(self):
        user_data = {
            'username': self.username,
            'password': self.password,
            'password2': self.password,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

        response = self.client.post('/register', data=user_data)
        self.assertEqual(response.status_code, 201)

        created_user = User.objects.get(username=user_data['username'])

        self.assertEqual(created_user.username, user_data['username'])
        self.assertEqual(created_user.email, user_data['email'])

    def test_user_creation_invalid_data(self):
        invalid_user_data = {
            'username': 'testuser',
        }

        response = self.client.post('/register', data=invalid_user_data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username=invalid_user_data['username']).exists())

    def test_valid_login(self):
        self.test_user_creation()
        login_data = {
            "username": self.username,
            "password": self.password
        }

        response = self.client.post('/login', data=login_data)
        self.assertEqual(response.status_code, 200)
        self.token = response.data['token']

        user = User.objects.get(username=self.username)
        self.assertEqual(user.auth_token.key, self.token)

    def test_invalid_login(self):
        self.test_user_creation()

        invalid_login_data = {
            'username': 'testuser',
            'password': 'Invalid',
        }
        response = self.client.post('/login', data=invalid_login_data)
        self.assertEqual(response.status_code, 400)

    def test_logout(self):
        self.test_valid_login()

        response = self.client.post('/logout', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username=self.username)
        self.assertFalse(Token.objects.filter(user=user).exists())

    def test_user_info(self):
        self.test_valid_login()
        response = self.client.get('/user', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data["username"], self.username)
        self.assertEqual(response.data["first_name"], self.first_name)
        self.assertEqual(response.data["last_name"], self.last_name)
        self.assertEqual(response.data["id"], self.id)

        response = self.client.get('/user/1', HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.username)
        self.assertEqual(response.data["first_name"], self.first_name)
        self.assertEqual(response.data["last_name"], self.last_name)
        self.assertEqual(response.data["id"], self.id)

    def test_change_password(self):
        self.test_valid_login()
        new_password = 'NewPassword123'
        changed_password = {
            'old_password': self.password,
            'password': new_password
        }

        response = self.client.put(
            '/user/change_password',
            data=changed_password,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, 200)

        new_login_data = {
            "username": self.username,
            "password": new_password
        }
        response = self.client.post('/login', data=new_login_data)
        self.assertEqual(response.status_code, 200)
