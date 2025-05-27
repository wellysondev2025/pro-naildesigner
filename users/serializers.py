from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
import re

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'is_nail_designer', 'phone')

    def validate_phone(self, value):
        value = value.strip().replace(" ", "")
        if not re.match(r'^\+?\d{10,15}$', value):
            raise serializers.ValidationError("Telefone inválido. Use formato +5511999999999.")
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Este telefone já está em uso.")
        return value

    def validate(self, data):
        data['email'] = data['email'].lower().strip()
        data['phone'] = data['phone'].strip().replace(" ", "")
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            is_nail_designer=validated_data.get('is_nail_designer', False),
            phone=validated_data['phone']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_nail_designer', 'phone', 'phone_verified', 'email_verified')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_or_email = attrs.get("username")
        password = attrs.get("password")

        if "@" in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email.lower())
                username = user_obj.username
            except User.DoesNotExist:
                raise serializers.ValidationError("Email ou senha inválidos.")
        else:
            username = username_or_email

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Usuário ou senha inválidos.")

        data = super().validate({"username": username, "password": password})
        return data
