"""fyp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [

    path('', views.Cover_page , name = 'cover_page'),
    path('find_my_product/', views.find_my_product, name='find_my_product'),
    path('api/Favourite/', views.Favourite_RestView.as_view()),
    path('api/user/', views.UserViewSet.as_view()),
    path('api/product/', views.RecentProductViewSet.as_view()),
    path('user/login/', views.user_login),
    path('user/logout/', views.user_logout),
    path('find_my_product/Search/',views.Searching_results)
    

]

