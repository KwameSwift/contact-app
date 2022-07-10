import os
from Auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from pathlib import Path

class TestDeleteRecords(APITestCase):
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

        self.client.post(path=reverse('Add New Record'),
                                data = {
                                    "phone_number": "123456789"
                                })
    # Delete a record
    def test_delete_record(self):
        delete_path = reverse('Delete Record', kwargs={
                           'record_id': 2
                       })
        response = self.client.delete(delete_path)
        expected_status_code = 200

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['message'], 'Record deleted successfully')

    # Delete a non-existing record
    def test_delete_non_existing_record(self):
        delete_path = reverse('Delete Record', kwargs={
                           'record_id': 100
                       })
        response = self.client.delete(delete_path)
        expected_status_code = 313

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['detail'], 'Record does not exist')
        