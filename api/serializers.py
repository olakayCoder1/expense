from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.conf import settings




Users = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['username', 'email']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'type':'password'},write_only=True)
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only': True},
        }



        def save(self):
            username = self.validated_data['username']
            email = self.validated_data['email']
            password = self.validated_data['password']
            password2 = self.validated_data['password2']
            user = Users(username=username , email=email)
            if password != password2 :
                raise serializers.ValidationError({'password': 'Password does not match'})
            if Users.objects.filter(username=username).exists():
                raise serializers.ValidationError({'username': 'Username already exist'})
            user.set_password(password)
            user.save()
            return user
