from django.shortcuts import render_to_response
import requests
import re
from collections import OrderedDict
import xlwt
from urllib.request import urlretrieve
import os
import random
import sys
from  pyquery import PyQuery as pq


def crawler_dcfever():
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
            tag.append('dcfever')
        return images, urls, names, prices, tag



def crawler_carousell():
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
        print(datas)
        for i in datas:
                    #print(i)
            images.append(i[1])
            a = i[2].replace(' ','-')
            urls.append('https://hk.carousell.com/p/'+a+'-'+i[0])
            names.append(i[2])
            prices.append(i[3])
            tag.append('carousell')


        return images, urls, names, prices, tag
def recent_crawler():
    dclink,dcurl , dcname, dcmoney, dctag = crawler_dcfever()
    calink,caproduct_links,caproduct_names,caproduct_moneys,catag = crawler_carousell()
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

