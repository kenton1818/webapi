from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from .models import User , My_Favourite


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email', 'password1', 'password2', )
class EditProfileForm(UserChangeForm):
    template_name='/something/else'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )

    
class Create_likeProduct(UserChangeForm):
    template_name='/something/else'

    class Meta:
        model = My_Favourite
        fields = (
            'user',
            'product_link',
            'product_name',
            'product_price'
        )