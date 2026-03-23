from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.ru',
            password='pass123456'
        )
        self.url = '/api/users/login/'

    def test_login_success(self):
        data = {'email': 'test@test.ru', 'password': 'pass123456'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_password(self):
        data = {'email': 'test@test.ru', 'password': 'pass'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
