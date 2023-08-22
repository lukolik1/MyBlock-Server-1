import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from .forms import LoginForm
from .castomUser import CustomUser, CustomUserManager

User = get_user_model()

class BlockSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser 
        fields = [ 'username', 'email', 'password', 'password2']  
        extra_kwargs = {'password': {'write_only': True}}

    
    
    email = serializers.EmailField()  # Adding the email field
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password and password2 and password != password2:
            raise serializers.ValidationError("Passwords don't match")

        return data

    def create(self, validated_data):
        user_manager = CustomUserManager()
        username = validated_data.get('username')
        email = validated_data.get('email')
        user = user_manager.create_user(username=username, email=email, **validated_data)
        return user







class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model.objects.create_user(password=password, **validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        form = LoginForm(data)
        if form.is_valid():
            return data
        else:
            errors = form.errors
            raise serializers.ValidationError(errors)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password1', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        password1 = data.get('password')
        password2 = data.get('password2')

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(_("Passwords don't match"))

        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginFormDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



