import os
from Auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from pathlib import Path

class TestAddRecords(APITestCase):
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
    
    # Test add new record
    def test_add_new_record(self):
        add_path = reverse('Add New Record')
        data = {
            "phone_number" : '0022447788',
            "user": self.user
        }
        response = self.client.post(add_path, data)
        expected_status_code = 201

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['message'], 'Record created successfully')

    # Test add already existing record
    def test_add_already_existing_record(self):
        add_path1 = reverse('Add New Record')
        data = {
            "phone_number" : '0022447788',
            "user": self.user
        }
        self.client.post(add_path1, data)

        add_path2 = reverse('Add New Record')
        data = {
            "phone_number" : '0022447788',
            "user": self.user
        }
        response = self.client.post(add_path2, data)

        expected_status_code = 311

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['status'], 'Error')
        self.assertEqual(response.json()['detail'], 'Phone number already exists')


    # Test add record without phone number
    def test_add_record_without_request_data(self):
        add_path = reverse('Add New Record')

        response = self.client.post(add_path)
        expected_status_code = 309

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['status'], 'Error')
        self.assertEqual(response.json()['detail'], 'phone_number is required')

    
    # Test add record with empty phone number
    def test_add_record_with_empty_phone_number(self):
        add_path = reverse('Add New Record')
        data = {
            "phone_number": ""
        }

        response = self.client.post(add_path, data)
        expected_status_code = 309

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['status'], 'Error')
        self.assertEqual(response.json()['detail'], 'phone_number is required')


    # Test add record without first_name
    def test_add_record_without_first_name(self):
        add_path = reverse('Add New Record')
        data = {
            "phone_number" : '0011223344',
            "last_name": 'Kofi',
            "middle_name": 'Koko',
            "address": 'Kumasi',
            "user": self.user
        }

        response = self.client.post(add_path, data)
        expected_status_code = 201

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['status'], 'Success')
        self.assertEqual(response.json()['message'], 'Record created successfully')

    # Test add record without last_name
    def test_add_record_without_last_name(self):
        add_path = reverse('Add New Record')
        data = {
            "phone_number" : '0011223345',
            "first_name": 'Kofi',
            "middle_name": 'Koko',
            "address": 'Kumasi',
            "user": self.user
        }

        response = self.client.post(add_path, data)
        expected_status_code = 201

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['status'], 'Success')
        self.assertEqual(response.json()['message'], 'Record created successfully')

    # Test add record without middle_name
    def test_add_record_without_middle_name(self):
        add_path = reverse('Add New Record')
        data = {
            "phone_number" : '0011223346',
            "first_name": 'Kofi',
            "last_name": 'Koko',
            "address": 'Kumasi',
            "user": self.user
        }

        response = self.client.post(add_path, data)
        expected_status_code = 201

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['status'], 'Success')
        self.assertEqual(response.json()['message'], 'Record created successfully')

    # Test add record without address
    def test_add_record_without_address(self):
        add_path = reverse('Add New Record')
        data = {
            "phone_number" : '0011223347',
            "first_name": 'Kofi',
            "last_name": 'Koko',
            "middel_name": 'Kumah',
            "user": self.user
        }

        response = self.client.post(add_path, data)
        expected_status_code = 201

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['status'], 'Success')
        self.assertEqual(response.json()['message'], 'Record created successfully')