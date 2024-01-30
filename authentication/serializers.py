from .models import  User  
from .tasks import password_reset_task


from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import smart_str, force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode


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
        



#! Serializer for User Login
class UserLoginSerializer(ModelSerializer):
    email=serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type':'password'}
    )
    

    class Meta:
        model=User
        fields=['email','password']




#! Serializer for Changing Password
class UserChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )
    new_password=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirmation=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )
    

    def validate_old_password(self,value):
        """
        Method which Validate old password of 
        User before Changing it 
        """
        user = self.context["user"]

        if not user.check_password(value):
            raise ValidationError(_("Current password doesn't match"))
        return value
    
    
    def validate(self, attrs):
        """
        Method which validate the new password and new 
        password confirmation and  Set new password for
        the user
        """
        old_password=attrs.get('old_password')
        new_password=attrs.get('new_password')
        new_password_confirmation=attrs.get('new_password_confirmation')

        if new_password != new_password_confirmation:
            raise ValidationError(_('Two Passwords does not match'))
        
        if old_password==new_password:
            raise ValidationError(_('New passwords cannot be similar to current password '))
        
        user=self.context['user']
        user.set_password(new_password)
        user.save()

        return attrs



#! Serializer for Sending Password Reset Email
class SendResetPasswordEmailSerializer(serializers.Serializer):
      email=serializers.EmailField()


      def validate(self, attrs):
        """
        Check If The Provided Email Is Registered or 
        not and if yes it also sends  a reset link  that email 
        """
        email=attrs.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User with the given email doesn't exist"))
        
        # Create unique uid and token for the specific user 
        uid=urlsafe_base64_encode(force_bytes(user.id))
        token=PasswordResetTokenGenerator().make_token(user)
        link=f'http://127.0.0.1:8000/auth/api/reset-password/{uid}/{token}/'
        subject="Resetting Password"
        email=user.email

        data={
            "subject":subject,
            "link":link,
            "to_email":email
        }

        # Celery Task Called  Here To send an Email
        password_reset_task.delay(data)

        return attrs
       



#! Serializer for Resetting Password 
class PasswordResetSerializer(serializers.Serializer):
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


    def validate(self, attrs):
        """
        Validate UID and Token from url params
        and set new passsword for the user
        """
        password=attrs.get('password')
        password_confirmation=attrs.get('password_confirmation')
        
        # Gets the uid and token passed from PasswordResetView
        uid=self.context['uid']
        token=self.context['token']
        id=smart_str(urlsafe_base64_decode(uid))

        # Validates password and password_confirmation
        if password != password_confirmation:
            raise serializers.ValidationError(_("Two password field doesn't match"))
         
        #  Checks that token is valid and not expired
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User not found"))
        
        # This checks wheather if the token created for the specific user
        # is changed or expired or not 
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError(_("Token Expired or Invalid"))
        
        # If everyvalidation is passed it set the new password for the user 
        user.set_password(password)
        user.save()

        return attrs