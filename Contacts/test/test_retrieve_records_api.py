import os
from Auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from pathlib import Path

class TestRetrieveRecords(APITestCase):
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

    


    def test_retrieve_paginated_records(self):
        retrieve_path = reverse('Retrieve All Records', kwargs={
                           'page_number': 1
                       })
        response = self.client.get(retrieve_path)
        expected_status_code = 200

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['status'], 'Success')


    def test_retrieve_existing_single_record(self):
        retrieve_path = reverse('Get Record', kwargs={
                           'record_id': 1
                       })
        response = self.client.get(retrieve_path)
        expected_status_code = 200

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['status'], 'Success')

    def test_retrieve_non_existing_single_record(self):
        retrieve_path = reverse('Get Record', kwargs={
                           'record_id': 10
                       })
        response = self.client.get(retrieve_path)
        # print(response.json())
        expected_status_code = 313

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['detail'], 'Record does not exist')

    

        
