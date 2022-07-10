from django import forms
from django.http import JsonResponse
from Auth.models.user import User
from Auth.serializers.auth_serializer import UserAuthenticationSerializer
from Auth.views.token_obtain_view import MyTokenObtainPairView
from helpers.validations import validate_email, check_parameters
from rest_framework import serializers
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework import status
from helpers.status_codes import UserAlreadyExists

class AddUser(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        new_email = str(email).lower()

        # Check if request has both password and email
        check_parameters(email, 'email')
        check_parameters(password, 'password')
            
        validate_email(new_email)
        

        try:
            User.objects.get(email=new_email)
            raise UserAlreadyExists()
        except User.DoesNotExist:
            if(len(password) >= 6):
               
                details = {
                    "email": new_email,
                    "password": make_password(password),
                }
                User.objects.create(**details)
                return JsonResponse({'status': 'success', "code": "201", 'detail': 'User created'}, status=status.HTTP_201_CREATED, safe=False) 
            else:
                default_detail = {
                    'status': 'failure',
                    'detail': 'Minimum 6 Characters'
                }
                raise serializers.ValidationError(default_detail)
     
  

class Authentication(MyTokenObtainPairView):
    serializer_class = UserAuthenticationSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)