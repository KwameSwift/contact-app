import os
from Auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from pathlib import Path

class TestRecordsWithoutAuthentication(APITestCase):
    def setUp(self):
        self.message = 'Authentication credentials were not provided.'
    # Delete a record without authentication
    def test_delete_record_without_authentication(self):
        delete_path = reverse('Delete Record', kwargs={
                           'record_id': 2
                       })
        response = self.client.delete(delete_path)
        expected_status_code = 401

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['detail'], self.message)


    # Add a record without authentication
    def test_add_record_without_authentication(self):
        add_path = reverse('Add New Record')
        data = {
            "phone_number" : '0022447788'
        }
        response = self.client.post(add_path, data)
        expected_status_code = 401

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['detail'], self.message)

    # Retrieve a record without authentication
    def test_retrieve_all_records_without_authentication(self):
        retrieve_path = reverse('Retrieve All Records', kwargs={
                           'page_number': 1
                       })
        response = self.client.get(retrieve_path)
        expected_status_code = 401

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['detail'], self.message)
        

    # Retrieve a record without authentication
    def test_retrieve_record_without_authentication(self):
        retrieve_path = reverse('Get Record', kwargs={
                           'record_id': 1
                       })
        response = self.client.get(retrieve_path)
        expected_status_code = 401

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['detail'], self.message)

    # Update a record without authentication
    def test_rupdate_record_without_authentication(self):
        retrieve_path = reverse('Update Record', kwargs={
                           'record_id': 1
                       })
        response = self.client.put(retrieve_path)
        expected_status_code = 401

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()['detail'], self.message)