import os
from Auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from pathlib import Path


class TestFileUpload(APITestCase):
    def setUp(self):
        self.email = "someone@gmail.org"
        self.password = "password"
        self.user = User.objects.create_user(
            email=self.email, password=self.password)

        token = self.client.post(
            path=reverse('Login'),
            data={
                'email': self.email,
                'password': self.password
            }
        )
        self.token = token.data['data']
        # print(self.token["access"])
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}'
        )

    # Test CSV file upload
    def test_file_upload(self):
        upload_path = reverse('Upload CSV')
        my_file = open('Contacts/test/test_data/test_data.csv', 'r')
        response = self.client.post(upload_path, {'csv':my_file})
        print(response.json())

        expected_status_code = 200

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['status'], 'Success')
        self.assertEqual(response.json()['message'], 'Data uploaded to database successfully')

    # Test CSV file upload with wrong key name for file
    def test_file_upload_with_wrong_key(self):
        upload_path = reverse('Upload CSV')
        my_file = open('Contacts/test/test_data/test_data.csv', 'r')
        response = self.client.post(upload_path, {'file':my_file})

        expected_status_code = 318

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['status'], 'Error')
        self.assertEqual(response.json()['detail'], 'Key error')