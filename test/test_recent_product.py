from mixer.backend.django import mixer
import pytest
from django.test import TestCase
from cover_page.models import  User, Product, My_Favourite
from cover_page.forms import SignUpForm , EditProfileForm , Create_likeProduct

class User_Model_test(TestCase):
    def setUp(self):
        data = {'first_name':"test123", 'last_name':"test123", 'email':"test@gmail.com", 'password2':"zz29332933", 'password1':"zz29332933"}
        form = SignUpForm(data = data)
        user = form.save(commit=False)    
        user.is_active = True
        user.save()
 
    def test_animals_can_speak(self):
        testProduct = User.fun_raw_sql_query(email="test@gmail.com")
        self.assertEqual(testProduct[0].first_name, 'test123')



class Product_Model_test(TestCase):
    def setUp(self):
        Product.objects.create(product_link="test.com", product_image_link="testimgae.com",product_name="test1",product_price="1000",product_tag="testtage") 
        
 
    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        testProduct = Product.sql_all_recent_product(product_tag = 'testtage')
        self.assertEqual(testProduct[0].product_price, '1000')
        self.assertEqual(testProduct[0].product_image_link, 'testimgae.com')
        self.assertEqual(testProduct[0].product_name, 'test1')
        self.assertEqual(testProduct[0].product_link, 'test.com')
