from rest_framework import serializers
from django.contrib.auth.models import User

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
        
        return validated_data