import requests
import re
from collections import OrderedDict
import xlwt
from urllib.request import urlretrieve
import os
import winsound


def download(url , name, money, date, search_keyword):

    if not os.path.exists(search_keyword):
            os.mkdir(search_keyword)
       
    
    for i in range(len(money)):
            if url[i] == "/images/s.gif":
                url[i]= "https://www.dcfever.com/images/s.gif"
            img = requests.get(url[i], timeout = 5000).content
            image_format = url[i].split('.')[-1]
            combina_formate = name[i]+"."+image_format
            filename = os.path.join(search_keyword , combina_formate)
            with open(filename,'wb') as f:
                f.write(img)

def crawler_dcfever(search_keyword, total_search, min_price,max_price):
    for i in str(total_search):
        search_url = "https://www.dcfever.com/trading/search.php?keyword="+str(search_keyword)+"&token=ewqeeppepppwewqqr&cat=all&type=sell&min_price="+min_price+"&max_price="+max_price+"&page="+str(total_search)
        r = requests.get(search_url)
        html = ""
        html = r.text
        data = re.findall(r'itemID=(\d*?)">.*?img src="(https://cdn10.dcfever.com/media/trading/.*?|/images/s.gif)".*?class=tlist_title>(.*?)</a>.*?tlist_price">(.*?)</td>.*?td>(\d.*?\s\d.*?:\d.*?)</t.*?',html)
        link = [k.replace(k,"https://www.dcfever.com/trading/view.php?itemID="+k) for j in data for k in j[::5]]
        url = []
        name = []
        money = []
        date = []
        print("pharsing........")
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
        name = [i.replace('/'," and ") for i in name]
        link = [i.replace(i,"https://www.dcfever.com/trading/view.php?itemID="+i) for i in link]
        download(url , name, money, date, search_keyword)
        return (data)

   

def search_start(search_keyword, total_search = 1, min_price="",max_price=""):
    data = []
    data = crawler_dcfever(search_keyword, total_search , min_price,max_price)
    return data


if __name__ =='__main__':
    search_start()
