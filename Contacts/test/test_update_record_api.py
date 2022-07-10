import os
from Auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from pathlib import Path

class TestUpdateRecords(APITestCase):
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
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}'
        )

        self.client.post(path=reverse('Add New Record'),
                                data = {
                                    "phone_number": "123456789"
                                })
    # Update a record
    def test_update_record(self):
        update_path = reverse('Update Record', kwargs={
                           'record_id': 1
                       })
        data = {
            "phone_number" : '0022447788'
        }
        response = self.client.put(update_path, data)
        expected_status_code = 200

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['message'], 'Record updated successfully')
    
    # Update a non-existing record
    def test_updatenon_existing__record(self):
        update_path = reverse('Update Record', kwargs={
                           'record_id': 100
                       })
        data = {
            "phone_number" : '0022447788'
        }
        response = self.client.put(update_path, data)
        expected_status_code = 313

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['detail'], 'Record does not exist')