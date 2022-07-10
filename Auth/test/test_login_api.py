from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from Auth.models import User


class LoginTest(APITestCase):
    url = reverse('Login')

    headers = {
        "Allow": "POST, OPTIONS",
        "Content-Type": "application/json",
        "Vary": "Accept"
    }
    mock_user_object = {
        "email": "surajabdul88@gmail.com",
        "password": "password1"
    }
    def create_user(self, email, password):
        user = User.objects.create_user(
            email=email, password=password
        )
        return user


    def test_login_with_correct_email_and_correct_password(self):
        """
        Test to assert a success login with correct email and password
        """
        # Create a user for in the test database for the login
        self.create_user("surajabdul88@gmail.com", 'password1')
        # Preparation: define url, headers, data, response

        data = {
            "password": "password1",
            "email": "surajabdul88@gmail.com"
        }

        response = self.client.post(
            path=self.url,
            data=data,
            format='json',
            headers=self.headers
        )
        expected_status = status.HTTP_200_OK
        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(response.data['detail'], "Login successful")

        
    def test_login_with_wrong_email_and_correct_password(self):
        """
        Test to assert a failed login with invalid wrong email but correct password
        """
        # Create a user for in the test database for the login
        self.create_user('surajabdul88@gmail.com', 'password1')
        # Preparation: define url, headers, data, response

        data = {
            "password": "password1",
            "email": "wrongemail@gmail.com"
        }

        response = self.client.post(
            path=self.url,
            data=data,
            format='json',
            headers=self.headers
        )
        expected_status = 312
        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(response.data['detail'], "User does not exist")

    def test_login_with_correct_email_and_wrong_password(self):
            """
            Test to assert a failed login with correct email but wrong password
            """
            # Create a user for in the test database for the login
            self.create_user('surajabdul88@gmail.com', 'password1')
            # Preparation: define url, headers, data, response

            data = {
                "password": "wrongpassword",
                "email": "surajabdul88@gmail.com"
            }

            response = self.client.post(
                path=self.url,
                data=data,
                format='json',
                headers=self.headers
            )
            expected_status = status.HTTP_401_UNAUTHORIZED
            self.assertEqual(response.status_code, expected_status)
            self.assertEqual(response.data['detail'], "No active account found with the given credentials")

    def test_login_with_wrong_email_wrong_password(self):
            """
            Test to assert a failed login with wrong email and wrong password
            """
            # Create a user for in the test database for the login
            self.create_user('surajabdul88@gmail.com', 'password1')
            # Preparation: define url, headers, data, response

            data = {
                "password": "wrongpassword",
                "email": "wrongemail@gmail.com"
            }

            response = self.client.post(
                path=self.url,
                data=data,
                format='json',
                headers=self.headers
            )
            expected_status = 312
            self.assertEqual(response.status_code, expected_status)
            self.assertEqual(response.data['detail'], "User does not exist")
