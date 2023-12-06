from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('first_name','last_name','username','email')

