from django.http import QueryDict
from django.views.generic import View
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response                            
from django.shortcuts import redirect, render
from mongoengine import *
import requests
import re
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from django import db
from django.contrib.auth import logout
from collections import OrderedDict
from django.views.decorators.csrf import csrf_exempt
import xlwt
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
import json
from rest_framework.decorators import list_route
from urllib.request import urlretrieve
from django.core import serializers
import os
import random
import sys
import time
from  pyquery import PyQuery as pq
import random
from django.contrib import auth
from django.urls import reverse
print(os.listdir())
from cover_page.forms import SignUpForm , EditProfileForm , Create_likeProduct
from cover_page.models import User , Product, My_Favourite
from rest_framework.decorators import api_view, renderer_classes
from cover_page.serializers import UserSerializer , ProductSerializer
# Create your views here.
from rest_framework import viewsets


def Cover_page(request):
    return render(request,'index.html', {})

def find_my_product(request):
    images, urls, names, prices, tags = recent_crawler()
    product_datas = [i for i in zip(images,urls,names,prices,tags)]
    context = {}
    product_datas = random.sample(product_datas,len(product_datas)) 
    context['product_datas'] = product_datas
    context["no_picture"] = "/images/s.gif"
    context['length'] = len(tags)
    return render(request,"search.html", context)

# Create your views here.

class UserViewSet(APIView):
    # /api/music/raw_sql_query/
        
    def delete(self,request):  
        print("delete")  
        try:
            print("delete   1",request.user.email)
            u = User.objects.get(email = request.user.email)
            u.delete()
            return Response({'status':'delete success','message':""}, status=status.HTTP_200_OK)
        except Exception as e :
            print("delete   2" , e)
            return Response({'status':'delete false','message':"The user not found"}, status=status.HTTP_200_OK)
            

    def get(self, request):
        try:
            user = self.request.user
            return Response({'status':'info success','message':{'userId':user.id,'UserEmail':user.email,'UserFirstName':user.first_name,'UserLastName':user.last_name,'UserIsSuper':user.is_superuser,'UserDataJoined':user.date_joined,'UserLastLogin':user.last_login}}, status=status.HTTP_200_OK)
            
            
        except :
            return Response({'status':'info false','message':'please login first'}, status=status.HTTP_200_OK)


    
    
    def post(self, request):
        #email = User.fun_raw_sql_query(email=email)
        print('request',request)
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print('fname',fname)
        print('lname',lname)
        print('email',email)
        print('password1',password1)
        print('password2',password2)
        data = {'first_name':fname, 'last_name':lname, 'email':email, 'password2':password2, 'password1':password1}
        form = SignUpForm(data = data)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            email = User.fun_raw_sql_query(email=email)
            serializer = UserSerializer(email, many=True)
            return Response({'status':'register success', 'message':serializer.data}, status=status.HTTP_200_OK)
        else:
            print(form.errors)
            return Response({'status':'register false', 'message':form.errors}, status=status.HTTP_200_OK)
    
    
    
    def put(self, request):
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        
        email = User.objects.get(email = request.user.email)
        
        existing_pw = request.POST.get('existing_pw')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        data = {'first_name':fname, 'last_name':lname, 'email':email, 'password2':password2, 'password1':password1}
        user = authenticate(email=email, password=existing_pw)
        if user is not None:
            form = SignUpForm(data, instance=request.user)
            if form.is_valid():
                
                user = form.save()
                
                return Response({'status':'update success', 'message':''}, status=status.HTTP_200_OK)
            else:
                print('form not ok')
                return Response({'status':'password comfirm false', 'message':form.errors}, status=status.HTTP_200_OK)
            
        else:
            return Response({'status':'password falas', 'message':'existing password is not match'}, status=status.HTTP_200_OK)
  
@api_view(['POST'])
def user_logout( request ):
        # simply delete the token to force a login
        logout(request)
        return Response({'status':'logout success', 'message':""}, status=status.HTTP_200_OK)
@api_view(['POST'])
def user_login( request):
        email = request.POST.get('email',None )
        password = request.POST.get('password', None )
        print(email)
        print(password)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                email = User.fun_raw_sql_query(email=email)
                serializer = UserSerializer(email, many=True)
                login(request, user)
                return Response({'status':'login success', 'message':serializer.data}, status=status.HTTP_200_OK)
        else:
                return Response({'status':'login falas', 'message':'no match any account'}, status=status.HTTP_200_OK)
    
    
class Favourite_RestView(APIView):
      
    def delete(self, request,):
        delete = QueryDict(request.body)
        pk = delete.get('pk')
        # delete an object and send a confirmation respons
        print(pk)
        My_Favourite.objects.get(pk = pk).delete()
        response = Response(
                        {"status":'delete success',},
                        content_type="application/json",
                        status=status.HTTP_200_OK,
                    )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response
            
    def post(self, request):
            if request.user.is_authenticated:
                print("is User");
                price = request.POST.get('price')
                name = request.POST.get('name')
                link = request.POST.get('link')
                My_Favourite.objects.create(user = request.user ,product_name = name,  product_link = link, product_price = price)
                response = Response(
                        {"status":'add success',"message":{"price":price,"name":name,"link":link}},
                        content_type="application/json",
                        status=status.HTTP_200_OK,
                    )
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                return response
            else:
                print("not login")
                response = Response(
                            {"status":'add false',"message":"please login"},
                            content_type="application/json",
                            status=status.HTTP_200_OK,
                        )
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                return response
       
    def get(self, request):
        print("is User");
        user = request.user
        print(user)
        context = My_Favourite.objects.values('product_name','product_link','product_price',"pk").filter(user = user)
        count = My_Favourite.objects.filter(user = user).count()
        data = list(context)
        if count == 0 :
            response = Response(
                    {"status":'get MYFavourite success',"message":"no record"},
                    content_type="application/json",
                    status=status.HTTP_200_OK,
                )
        else:
                    
            response = Response(
                    {"status":'get MYFavourite success',"message":data},
                    content_type="application/json",
                    status=status.HTTP_200_OK,
                )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response



@csrf_exempt
@api_view(['GET'])
def Searching_results(request):
            request.encoding='utf-8'
            #if  request.GET:
            #    keyword = request.GET.get('keyword', None)
            keyword = request.GET.get('keyword', "")
            seach_type = request.GET.get('seach_type', "")
            minarea = request.GET.get('minarea', "")
            maxarea = request.GET.get('maxarea', "")
            page = request.GET.get('page', "0")
            page = int(page)+1
            print('seach_type',seach_type)
            links,url , name, money, date , tag, next_page = Search_start(keyword,  minarea, maxarea,seach_type,page)
            
            index = [i for i in range(0,len(links))]
            contexts = []
            print(tag)
            for i in range(0,len(url)):
                if url[i] == '/images/s.gif':
                    url[i]='https://www.dcfever.com/images/s.gif'
                context = {"url":url[i],"name":name[i],"product_links":links[i],"product_price":money[i],"date":date[i], "tag": tag[i]}
                contexts.append(context)
            data = zip(contexts)
            response = Response(
                    {"status":'search success',"next_page":next_page,"length":len(contexts),"search_keyword":keyword,"message":{"search_keyword":keyword,"result":data}},
                    content_type="application/json",
                    status=status.HTTP_200_OK,
                )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            print(len(tag))
            return response
            #data = {"status":'search success',"message":{"search_keyword":keyword,"result":data}}
            #return Response(data)
'''
class RecentProductViewSet(APIView):
    
    def get(self, request):
        Product.del_recent_product()
        product_link, product_image_link, product_name, product_price, product_tag = recent_crawler()
        
        product_info = list(zip(product_link, product_image_link, product_name, product_price, product_tag))
        for i in product_info:
            Product.objects.create(product_link=i[1], product_image_link=i[0],product_name=i[2],product_price=i[3],product_tag=i[4]) 
        Dcfever_result = Product.sql_all_recent_product(product_tag = 'Dcfever')
        Dcfever_serializer = ProductSerializer(Dcfever_result,many=True)
        Carousell_result = Product.sql_all_recent_product(product_tag = 'Carousell')
        Carousell_serializer = ProductSerializer(Carousell_result,many=True)
        print('============')
        return Response({'status':'success', 'message':{'Carousell':Carousell_serializer.data,'Dcfever':Dcfever_serializer.data}}, status=status.HTTP_200_OK)
'''     
 

class RecentProductViewSet(APIView):
    def put(self, request):
        total = Product.sql_all_recent_product(product_tag = "Dcfever")
        if len(total) == 0:
            return Response({'status':'fails', 'message':' recent product table is null'}, status=status.HTTP_200_OK)
     
        Product.del_recent_product()
        product_link, product_image_link, product_name, product_price, product_tag = recent_crawler()
        product_info = list(zip(product_link, product_image_link, product_name, product_price, product_tag))
        for i in product_info:
            Product.objects.create(product_link=i[1], product_image_link=i[0],product_name=i[2],product_price=i[3],product_tag=i[4]) 
        
        return Response({'status':'success', 'message':' recent product table update success'}, status=status.HTTP_200_OK)
     
    def get(self, request):
        Dcfever_result = Product.sql_all_recent_product(product_tag = 'Dcfever')
        Dcfever_serializer = ProductSerializer(Dcfever_result,many=True)
        Carousell_result = Product.sql_all_recent_product(product_tag = 'Carousell')
        Carousell_serializer = ProductSerializer(Carousell_result,many=True)
        print(Dcfever_result.count())
        print(Carousell_result.count())
        if Dcfever_result.count() == 0 and Carousell_result.count() == 0:
            return Response({'status':'false', 'message':'the recent product table is null'}, status=status.HTTP_200_OK)
        else:
            return Response({'status':'success', 'message':{'Carousell':Carousell_serializer.data,'Dcfever':Dcfever_serializer.data}}, status=status.HTTP_200_OK)
     
    
    

    def post(self, request):

        product_link, product_image_link, product_name, product_price, product_tag = recent_crawler()
        
        product_info = list(zip(product_link, product_image_link, product_name, product_price, product_tag))
        for i in product_info:
            Product.objects.create(product_link=i[1], product_image_link=i[0],product_name=i[2],product_price=i[3],product_tag=i[4]) 
        Dcfever_result = Product.sql_all_recent_product(product_tag = 'Dcfever')
        Dcfever_serializer = ProductSerializer(Dcfever_result,many=True)
        Carousell_result = Product.sql_all_recent_product(product_tag = 'Carousell')
        Carousell_serializer = ProductSerializer(Carousell_result,many=True)
        return Response({'status':'create recent product success', 'message':{'Carousell':Carousell_serializer.data,'Dcfever':Dcfever_serializer.data}}, status=status.HTTP_200_OK)
     
    
   
def download(url , name, money, date, search_keyword):

    if not os.path.exists(search_keyword):
            os.mkdir(search_keyword)
       
    
    for i in range(len(money)):
            if url[i] == "/images/s.gif":
                url[i]= "https://www.dcfever.com/images/s.gif"
            img = requests.get(url[i], timeout = 5000).content
            image_format = url[i].split('.')[-1]
            mpa = dict.fromkeys(range(32))
            product_name = name[i].translate(mpa)
            
            combina_formate = product_name+"."+image_format
            filename = os.path.join(search_keyword,combina_formate)
            print(filename)
            try:
                
                with open(filename,'wb') as f:
                    f.write(img)
            except OSError:
                product_name = ""
                #error =  [r'/',r'\',r':',r'*',r'"',r'<',r">",r"|"]
                for i in combina_formate:
                    if i is "/":
                          product_name += ""
                    elif i is "\\":
                          product_name += ""
                    elif i is ":":
                          product_name += ""
                    elif i is "*":
                          product_name += ""
                    elif i is '"':
                          product_name += ""
                    elif i is "<":
                          product_name += ""
                    elif i is ">":
                          product_name += ""
                    elif i is "|":
                          product_name += ""
                    else:
                        product_name += i
                combina_formate = product_name+"."+image_format
                filename = os.path.join(search_keyword , combina_formate)
                with open(filename,'wb') as f:
                    f.write(img)

def crawler_dcfever(search_keyword, page, min_price,max_price,seach_type):
        if seach_type != None:
            search_url = "https://www.dcfever.com/trading/search.php?keyword="+str(search_keyword)+"&token=ewqeeppepppwewqqr&cat="+seach_type+"&type=sell&min_price="+min_price+"&max_price="+max_price+"&page="+str(page)
        else:
            search_url = "https://www.dcfever.com/trading/search.php?keyword="+str(search_keyword)+"&token=ewqeeppepppwewqqr&cat=all&type=sell&min_price="+min_price+"&max_price="+max_price+"&page="+str(page)
        r = requests.get(search_url)
        html = ""
        html = r.text   
        data = re.findall(r'itemID=(\d*?)">.*?img src="(https://cdn10.dcfever.com/media/trading/.*?|/images/s.gif)".*?class=tlist_title>(.*?)</a>.*?tlist_price">(.*?)</td>.*?td>(\d.*?\s\d.*?:\d.*?)</t.*?',html)
        link = [k.replace(k,"https://www.dcfever.com/trading/view.php?itemID="+k) for j in data for k in j[::5]]
        url = []
        name = []
        money = []
        date = []
        tag = []
        for first in data[::1]:
            for first_detail in range(len(first)):
                if first_detail == 1:
                    url.append(first[first_detail])
                if first_detail == 2:
                    name.append(first[first_detail])
                if first_detail == 3:
                    money.append(first[first_detail])
                if first_detail == 4:
                    date.append(first[first_detail])
                tag.append('dcfever')
        name = [i.replace('/'," and ") for i in name]
        #link = [i.replace(i,"https://www.dcfever.com/trading/view.php?itemID="+i) for i in link]
        #print(link)
        #download(url , name, money, date, search_keyword)
        return link,url , name, money, date,tag 
def crawler_carosell(search_keyword,  min_price,max_price,page):
        title = []
        link_urls = []
        image_urls = []
        USER_AGENTS = [
           {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36"},
           {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)"},
           {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"},
           {"User-Agent":"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"},
           {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)"},
           {"User-Agent":"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)"},
           {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)"},
           {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)"},
           {"User-Agent":"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6"},
           {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1"},
           {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"},
           {"User-Agent":"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"},
           {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6"},
           {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"},
           {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20"},
           {"User-Agent":"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"}
           ]
    #obtain a request head randomly in each request
        randdom_header=random.choice(USER_AGENTS)
        headers = {
            'Host': 'hk.carousell.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': randdom_header['User-Agent']
        }
          #url，pass key_word and pn
        def url_format(session):
            url = 'https://hk.carousell.com'
            # static parameter
            url_format = url,session
            return url
         #
        def get_html(url):
            response = requests.get(url, headers=headers)
            response.encoding='utf-8'
            if response.status_code == 200:
                return response.text
            if response.status_code == 302:
                print('request error')
                time.sleep(10)
                response = requests.get(url, headers=headers)
                return response.text
        count = 0
        #print('start')
        for i in range(0,page):
            i += 1
            import time
            time.sleep(3)
            url="https://hk.carousell.com/search/products/?price_end="+str(max_price)+"&price_start="+str(min_price)+"&query="+str(search_keyword)
            res_html=get_html(url)
            doc=pq(res_html)
            next_page_session=doc('.pagination-next > a').attr('href')
            next_url=url_format(next_page_session)
            #next_page = 'https://hk.carousell.com'+next_page_session
            #print(next_page)
                        

            if i == page:
                r = requests.get(url)
                html = r.text
                non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                html_trans=html.translate(non_bmp_map)
                '''
                datas = re.findall(
        r'id":"(.*?)","'
                    , html_trans)
                print('id',datas)
                datas = re.findall(
        r'title":"(.*?)","description'
                    , html_trans)
                print('title',datas)
                datas = re.findall(
        r'primaryPhotoUrl":"(.*?)","primaryPhotoThumbnailUrl'
                    , html_trans)
                print('photo_image',datas)
                datas = re.findall(
        r'price":"(.*?)","priceFormatted'
                    , html_trans)
                print('price',datas)
                datas = re.findall(
        r'timeCreated":"(.*?)"'
                    , html_trans)
                print('time',datas)
                '''

                datas = re.findall(
        r'id":"([0-9]*?)","title":"(.*?)","description.*?primaryPhotoUrl":"(.*?)","primaryPhotoThumbnailUrl.*?price":"(.*?)","priceFormatted.*?timeCreated":"(.*?)"'
                    , html_trans)
                
                product_links = []
                product_names = []
                product_moneys = []
                product_create_dates = []
                product_image_links = []
                tag = []
                for i in datas:
                    #print(i)
                    for j in range(len(i)):
                        if j == 0:
                            a = i[1].replace('\u002F','-')
                            a = i[1].replace(' ','-')
                            product_links.append('https://hk.carousell.com/p/'+a+'-'+str(i[j]))
                        if j == 1:
                            a = i[1].replace('\u002F',' ')
                            product_names.append(a)
                        if j == 2:
                            product_image_links.append(i[j].replace('\\u002F','/'))
                        if j == 3:
                            product_moneys.append(i[j])
                        if j == 4:
                            product_create_dates.append(i[j])
                        tag.append('Carosell')
                '''print('product_links',product_links)
                print('')
                print('')
                print('product_name',product_names)
                print('')
                print('')
                print('product_moneys',product_moneys)
                print('')
                print('')
                print('product_image_links',product_image_links)
                print('')
                print('')
                print('product_create_dates',product_create_dates)
                print('')
                print('')
                '''
                #title.append(i)
                processed_date = []

                for i in product_create_dates:

                    a = i.split('T')
                    dates = a[0]
                    times = a[1]
                    date = '' 
                    time = ''
                    date += str(dates.split('-')[2])+'/'+str(dates.split('-')[1])
                    print(times)
                    time += str(times.split(':')[0])+':'+str(times.split(':')[1])
                    processed_date.append(date+' '+time)


        return (product_links, product_image_links,product_names,product_moneys,processed_date, tag)
                     
                        # no next page
            
def Search_start(keyword, min_price="",max_price="",seach_type=None ,page = 1,):
    data = []
    if seach_type == 'Photography':
        seach_type = '1'
    if seach_type == 'Computer':
        seach_type = '2'
    if seach_type == 'Audio':
        seach_type = '44'
    if seach_type == 'Game':
        seach_type = '43'
    if seach_type == 'Watch':
        seach_type = '99'
    if seach_type == 'Clothing':
        seach_type = '45'
    if seach_type == 'Electrical appliances':
        seach_type = '104'
    if seach_type == 'Mobile Communication':
        seach_type = '3'
    if seach_type == 'Mobile Communication':
        seach_type = '4'
    print('seach_type',seach_type)
    total_link = []
    total_url = []
    total_name = []
    total_money = []
    total_date = []
    total_tag = []
    total_next_page = []
    dclink,dcurl , dcname, dcmoney, dcdate , dctag = crawler_dcfever(keyword, page ,min_price,max_price, seach_type )
    calink,caproduct_links,caproduct_names,caproduct_moneys,caproduct_create_dates, ca_tag= crawler_carosell(keyword,min_price,max_price,page)
    for i in dclink:
        total_link.append(i)
    for i in calink:
        total_link.append(i)
    for i in dcurl:
        total_url.append(i)
    for i in caproduct_links:
        total_url.append(i)
    for i in dcname:
        total_name.append(i)
    for i in caproduct_names:
        total_name.append(i)
    for i in dcmoney:
        total_money.append(i)
    for i in caproduct_moneys:
        total_money.append(i)
    for i in dcdate:
        total_date.append(i)
    for i in caproduct_create_dates:
        total_date.append(i)
    for i in dctag:
        total_tag.append(i)
    for i in ca_tag:
        total_tag.append(i)
    
    next_page = page+1

    print(total_next_page)
    return (total_link,total_url , total_name, total_money, total_date, total_tag,next_page)
#dcfever_data = crawler_dcfever('iphone',1,'','')
#print(dcfever_data)
#print(Search_start('iphone'))


def recent_crawler_dcfever():
        prices = []
        images = []
        names = []
        urls = []
        tag = []
        search_url = "https://www.dcfever.com/trading/index.php"
        r = requests.get(search_url)
        html = ""
        html = r.text   

        '''
        <img src="(.*?)" *?view.php?itemID=(.*?)">(.*?)</a><br><span class="price">(.*?)</span>
        '''
        data = re.findall(r'<img src="(.*?)".*?itemID=(.*?)">(.*?)</a><br><span class="price">(.*?)</span>',html)
        for i in data:
            images.append(i[0])
            urls.append("https://www.dcfever.com/trading/view.php?itemID="+i[1])
            names.append(i[2])
            prices.append(i[3])
            tag.append('Dcfever')
        return images, urls, names, prices, tag



def recent_crawler_carousell():
        USER_AGENTS = [
           {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36"},
           {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)"},
           {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"},
           {"User-Agent":"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"},
           {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)"},
           {"User-Agent":"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)"},
           {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)"},
           {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)"},
           {"User-Agent":"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6"},
           {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1"},
           {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"},
           {"User-Agent":"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"},
           {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6"},
           {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"},
           {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20"},
           {"User-Agent":"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"}
           ]
    #obtain a request head randomly in each request
        randdom_header=random.choice(USER_AGENTS)
        headers = {
            'Host': 'hk.carousell.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': randdom_header['User-Agent']
        }
          #url，pass key_word and pn
        prices = []
        images = []
        names = []
        urls = []
        tag = []
        
        url = "https://hk.carousell.com/service/home/4.0/feed/?count=10&countryID=1819730&session="
        r = requests.get(url) 
        html = r.text
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        html_trans=html.translate(non_bmp_map)

        datas = re.findall(r'listingCard":{"id":"(.*?)".*?"photoUrls".*?"(.*?)"].*?"header_1","stringContent":"(.*?)"},{"component":"header_2","stringContent":"(.*?)"',html_trans)
        for i in datas:
                    #print(i)
            images.append(i[1])
            a = i[2].replace(' ','-')
            urls.append('https://hk.carousell.com/p/'+a+'-'+i[0])
            names.append(i[2])
            prices.append(i[3])
            tag.append('Carousell')
        if len(images) == 0:
            print('=========')
            #images, urls, names, prices, tag = recent_crawler_carousell()
            pass

        return images, urls, names, prices, tag
def recent_crawler():
    dclink,dcurl , dcname, dcmoney, dctag = recent_crawler_dcfever()
    try:
        calink,caproduct_links,caproduct_names,caproduct_moneys,catag = recent_crawler_carousell()
    except Exception as e :
        pass

    for i in caproduct_links:
        dcurl.append(i)
    for i in caproduct_names:
        dcname.append(i)
    for i in caproduct_moneys:
        dcmoney.append(i)
    for i in calink:
        dclink.append(i)
    for i in catag:
        dctag.append(i)
    return (dclink,dcurl , dcname, dcmoney,dctag)
#print(crawler_carosell("iphone", 100,200, page = 3))

