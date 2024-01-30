from .models import  User  

from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.password_validation import validate_password



from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError


#! Serializer for User Registration 
class UserRegistrationSerializer(ModelSerializer):
    password=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )
    password_confirmation=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )


    class Meta:
        model=User 
        fields=[
            'fullname',
            'email',
            'password',
            'password_confirmation'
        ]


    def validate(self, attrs):
        """
        Ensures the password and password_confirmation 
        passed to a serializer is the same
        """
        password=attrs.get('password')
        password_confirmation=attrs.get('password_confirmation')

        if password!= password_confirmation:
            raise serializers.ValidationError(_("Two Password doesn't match "))
        
        return attrs
    

    def create(self,validated_data):
        """
        Creates User instance using validated data
        """
        try:
            user=User.objects.create(
                fullname=validated_data['fullname'],
                email=validated_data['email'],
            )
            user.set_password(validated_data['password'])
            user.save()
            return user 
            
        except Exception as e:
            # For Debugging error if any exception occour
            print(f"Error alert--->{e}")

            raise ValidationError(_("Somme Error occoured during registration"))