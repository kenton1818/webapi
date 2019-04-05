from cover_page.models import User
from rest_framework import serializers
import requests
import re
import sys
import random
from rest_framework import serializers
from cover_page.models import User , Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ( 'first_name', 'last_name', 'email', 'password', )


    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        #fields = '__all__'
        fields = ( 'product_image_link','product_link', 'product_name', 'product_price', 'product_tag')
