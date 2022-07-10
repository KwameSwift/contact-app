from django.test import TestCase
from Auth.models import User
from django.db.utils import IntegrityError
from django.urls import reverse

class UserManagerTest(TestCase):
    def test_create_user(self):
        test_user = User.objects.create(
            email='surajabdul88@gmail.com', password='12345678'
        )
        self.assertEqual(test_user.email, 'surajabdul88@gmail.com')
        self.assertTrue(test_user.is_active)
        self.assertFalse(test_user.is_admin)
        self.assertIsNotNone(test_user.registration_date)