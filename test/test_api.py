from rest_framework import status
from rest_framework.test import APITestCase

from cover_page.models import  User, Product, My_Favourite
from cover_page.forms import SignUpForm , EditProfileForm , Create_likeProduct

class UserAPITests(APITestCase):
     
    def setUp(self) :
        data = {'first_name':"test123", 'last_name':"test123", 'email':"test123123123@gmail.com", 'password2':"zz29332933", 'password1':"zz29332933"}
        form = SignUpForm(data = data)
        user = form.save(commit=False)    
        user.is_active = True
        user.save()

    def test_app_user_signup_success(self):
        path = '/api/user/'
        data = {'first_name':"test123", 'last_name':"test123", 'email':"test123123@gmail.com", 'password2':"zz29332933", 'password1':"zz29332933"}
        response = self.client.post(path, data)
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK,)

    def test_app_user_login_success(self):
        path = '/user/login/'
        data = {'email':"test123123123@gmail.com", 'password':"zz29332933"}
        response = self.client.post(path, data)
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK,)
    def test_app_user_ld_success(self):
        path = '/api/Favourite/'
        data = {'price':"1000", 'name':"test_product","link":"test.com"}
        response = self.client.post(path, data)
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK,)