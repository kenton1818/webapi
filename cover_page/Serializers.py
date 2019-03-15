from cover_page.models import User
from rest_framework import serializers

from rest_framework import serializers
from cover_page.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ( 'first_name', 'last_name', 'email', 'password', )
