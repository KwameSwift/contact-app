from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class AddUserAPITest(APITestCase):
    api_url = reverse('Add User')
    headers = {
        "Allow": "POST, OPTIONS",
        "Content-Type": "application/json",
        "Vary": "Accept"
    }
    def setUp(self):
        self.data_1 = {
            'email': 'example@gmail.com',
            'password': '12345678'
        }
        self.user_1 = get_user_model().objects.create_user(**self.data_1)
        self.user_1.save()

    def test_account_creation_with_valid_email(self):
        """
        test a successful account creation
        with email, password
        """
        data = {
            'email': 'surajabdul88@gmail.com',
            'password': '12345678'
        }
        response = self.client.post(
            path=self.api_url,
            data=data,
            format='json',
            headers=self.headers
        )
        # Testing - response status, response body,
        # created objects at the database
        expected_status = status.HTTP_201_CREATED
        self.assertEqual(response.status_code, expected_status)
        # self.assertEqual(response.data['detail'], "User created")

    def test_account_creation_with_an_inavalid_email(self):
        data = {
            'email': 'surajabdul88@gmail',
            'password': '12345678'
        }
        response = self.client.post(
            path=self.api_url,
            data=data,
            format='json',
            headers=self.headers
        )
        # Testing - response status, response body,
        # created objects at the database
        expected_status = 310
        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(response.data['detail'], "Invalid email")


    def test_account_creation_with_an_inavalid_password(self):
        """
        let a creation fail by invalid password
        """
        data = {
            'email': 'suraj@gmail.com',
            'password': 'kW'
        }
        response = self.client.post(
            path=self.api_url,
            data=data,
            format='json',
            headers=self.headers
        )
        # Testing - response status, response body,
        # created objects at the database
        expected_status = status.HTTP_400_BAD_REQUEST
        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(response.data['detail'], "Minimum 6 Characters")

    def test_account_creation_with_an_email_that_exists(self):
        # create account
        data = {
            "email": "unverified@imboate.com",
            "password": "aegistest"
        }
        self.client.post(
            path=self.api_url,
            data=data,
            format='json',
            headers=self.headers
        )
        # try account creation again
        response = self.client.post(
            path=self.api_url,
            data=data,
            format='json',
            headers=self.headers
        )
        # Testing - response status, response body,
        # created objects at the database
        expected_status = 313
        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(response.data['detail'], "User already exists with same email")
