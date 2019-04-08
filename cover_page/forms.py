from django import forms

class LoginForm(forms.Form):
    usname = forms.CharField(label = 'username', required = True)
 #   email = forms.EmailField(label = 'email',required=True)
    psw = forms.CharField(label = 'password', widget = forms.PasswordInput)
'''    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = authenticate(username = username , password = password)
        if user is None:
            raise forms.ValidationError('username or password not correct')
        else:
            self.cleaned_data['user'] = user'''