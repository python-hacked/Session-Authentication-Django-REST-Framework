from rest_framework import serializers
from . models import *

class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['email','name','password','confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Password not confirm_password doesn't match.")
        return attrs
    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value
    
    def create(self,validated_data):
        user = User.objects.create(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password'],
        )
        user.is_active = False
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.save()
        return instance