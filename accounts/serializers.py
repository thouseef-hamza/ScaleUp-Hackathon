from rest_framework import serializers
from accounts.models import User

class RegisterationSerializer(serializers.Serializer):
    user_type_choices = ('researcher', 'healthprovider', 'patient')
    
    first_name=serializers.CharField(max_length=100)
    last_name=serializers.CharField(max_length=100,required=False)
    email=serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    user_type=serializers.ChoiceField(choices=user_type_choices)
    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            return serializers.ValidationError("User Already Registered")
        return value
    
    def validate_phone_number(self,value):
        if User.objects.filter(phone_number=value).exists():
            return serializers.ValidationError("User Already Registered")
        return value