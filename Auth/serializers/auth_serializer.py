from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from Auth.models.user import User
from helpers.status_codes import UserDoesNotExist

class SingleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class UserAuthenticationSerializer(TokenObtainPairSerializer):
    user = SingleUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        request = self.context["request"]
        request_data = request.data
        email = request_data.get('email')
        new_mail = str(email).lower()
        try:
            User.objects.get(email=new_mail)
        except User.DoesNotExist:
            raise UserDoesNotExist()

        data = super().validate(attrs)
        data['user'] = {
            'user_key': self.user.user_key,
            }
        return {'status':'success', 'detail': 'Login successful', 'data': data}

