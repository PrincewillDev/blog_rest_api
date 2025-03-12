from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class ResgisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    def validate(self, data):
        if User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('username already exist')

        if User.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError("email already exist")
        
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password must match")
        
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()  # Change from email to username
#     password = serializers.CharField()
        
#     def validate(self, data):
#         if not User.objects.filter(username=data['username']).exists():
#             raise serializers.ValidationError('account not found')
#         return data
    
#     def get_jwt_token(self, data):
#         user = authenticate(username=data['username'], password=data['password'])
        
#         if not user:
#             return {
#                 'message': 'invalid credential',
#             }
#         refresh = RefreshToken.for_user(user)
        
#         return {
#             'message': 'Login Success',
#             'data': {'token': {'refresh': str(refresh), 'access': str(refresh.access_token),} }
#         }
    
        