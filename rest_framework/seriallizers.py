from cover_page.models import User


class employeeSerializer(Serializers.ModelSeriallzer):
    class Meta:
        model = User
    fields = '__all__'