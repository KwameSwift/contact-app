from django.urls import path
from .views.auth_view import Authentication, AddUser



urlpatterns = [
    path('login/', Authentication.as_view(), name="Login"),
    path('add-user/', AddUser.as_view(), name='Add User'),
]
