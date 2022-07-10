from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from helpers.validations import validate_email
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email='',
                    password=None, 
                    ):

        """
        Creates and saves a User with the given email and password.
        """

        validate_email(email)

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        if not validate_email(email):
            raise TypeError('A user needs a valid Email Address')
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    user_key = models.UUIDField(
        unique=True,
        primary_key=True,
        default = uuid.uuid4,
    )

    email = models.EmailField(
        max_length=255,
        blank=True,
        unique=True
    )

    is_admin = models.BooleanField(
        default=False
    )
 
    is_active = models.BooleanField(
        default=True,
    )


    registration_date = models.DateTimeField(
        auto_now_add=True
    )

    
    # unique field
    USERNAME_FIELD = 'email'
    objects = UserManager()


    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, Auth):
        # "Does the user have permissions to view the app Auth?"
        # Simplest possible answer: Yes, always
        return True