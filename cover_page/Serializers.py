from cover_page.models import User
from rest_framework import serializers

class employeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    fields = '__all__'