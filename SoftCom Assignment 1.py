import requests
import bs4
import os
from pathlib import Path
import urllib.parse

def beautify(elem):
    text = ''
    for i in elem.children:
        if isinstance(i, bs4.NavigableString):
            text += i.replace("\n", "").strip()
        elif i.name == 'br':
            text += '\n'*2
    return text

def get_data(link): 
    try : 
        page = requests.get(link)
        soup = bs4.BeautifulSoup(page.content,"html.parser")
        title = soup.find("div", class_='_2NFXP').find('h1',class_='_23498').text 
        date = soup.find('div',class_='_3Mkg- byline').text.split("|")[-1].replace("Updated: ","").lstrip()
        text = beautify(soup.find("div",class_="ga-headlines"))
        return ['Title\n',title,'\n'*2,'Link\n',link,'\n'*2,'Date & Time\n',date,'\n'*2,'Text\n',text]
    except AttributeError:
        return ["Error, could not access anything at : ",link]
    except ConnectionError:
        return ["Error, could not access anything at : ",link]

def create_file(filename,data): 
    file = open(filename,'w')
    file.writelines(data)
    file.close()    

def make_folder(name):
    os.mkdir('./'+name)


def get_articles_india(link,foldername):
    
    page = requests.get(link)
    soup = bs4.BeautifulSoup(page.content,"html.parser")
    links1 = soup.find_all('div',{'id':'c_wdt_list_1'})
    links2=[]
    for i in links1:
        links2.extend(i.find_all('ul',class_="top-newslist clearfix"))
        links2.extend(i.find_all('ul',class_="list5 clearfix"))
        
    data = []
    for j in range(len(links2)):
        for i in links2[j].find_all('li'):
            if i.get('class') != ['prime']:
                temp=urllib.parse.urljoin("https://timesofindia.indiatimes.com",i.a.get('href'))
                data.append(get_data(temp))
                
    filenames=[]
    for i in range(1,len(data)+1):
        mainfolder = Path(foldername)
        filename = 'India_Article'+str(i)+'.txt'
        file = mainfolder / filename
        filenames.append(file)
    return(filenames,data)

def get_articles_world(link,foldername):
    
    page = requests.get(link)
    soup = bs4.BeautifulSoup(page.content,"html.parser")
    data =[get_data(urllib.parse.urljoin("https://timesofindia.indiatimes.com",i.span.a.get("href"))) for i in soup.find('div',class_='top-newslist').find_all('li')]
    data.extend([get_data(urllib.parse.urljoin("https://timesofindia.indiatimes.com",i.ul.li.span.a.get("href"))) for i in soup.find('div',class_='news-list1').find_all('div',class_='news_card')])
    
    filenames=[]
    for i in range(1,len(data)+1):
        mainfolder = Path(foldername)
        filename = 'World_Article'+str(i)+'.txt'
        file = mainfolder / filename
        filenames.append(file)
    return(filenames,data)

def get_articles_business(link,foldername):
    
    page = requests.get(link)
    soup = bs4.BeautifulSoup(page.content,"html.parser")
    data =[get_data(urllib.parse.urljoin("https://timesofindia.indiatimes.com",i.span.a.get("href"))) for i in soup.find('div',class_='top-newslist').find_all('li')]
    data.extend([get_data(urllib.parse.urljoin("https://timesofindia.indiatimes.com",i.span.a.get("href"))) for i in soup.find('div',class_='business_list').find_all('li')])
    data.extend([get_data("https://timesofindia.indiatimes.com"+i.span.a.get("href")) for j in soup.find_all('div',{'id':'c_budgetsectors_1'}) for i in j.find_all('li')])    
        
    filenames=[]
    for i in range(1,len(data)+1):
        mainfolder = Path(foldername)
        filename = 'Business_Article'+str(i)+'.txt'
        file = mainfolder / filename
        filenames.append(file)
    return(filenames,data)

def get_articles_home(link,foldername):
    
    page = requests.get(link)
    soup = bs4.BeautifulSoup(page.content,"html.parser").find('div',{'id':'content'}).find('div',class_='wrapper clearfix')
    data =[get_data(urllib.parse.urljoin("https://timesofindia.indiatimes.com",soup.find('div',class_='featured').a.get("href")))]
    data.extend([get_data(urllib.parse.urljoin("https://timesofindia.indiatimes.com",i.a.get("href"))) for i in soup.find('div',class_='top-story').find_all('li')])
    try :
        data.extend([get_data(urllib.parse.urljoin("https://timesofindia.indiatimes.com",i.a.get("href"))) for i in soup.find('div',{'id':'lateststories'}).find_all('li') if i.get('class') != ['prime']])    
    except AttributeError: 
        data.append("No data.")
           
    filenames=[]
    for i in range(1,len(data)+1):
        mainfolder = Path(foldername)
        filename = 'Home_Article'+str(i)+'.txt'
        file = mainfolder / filename
        filenames.append(file)
    return(filenames,data)



links=['https://timesofindia.indiatimes.com/india','https://timesofindia.indiatimes.com/world','https://timesofindia.indiatimes.com/business','https://timesofindia.indiatimes.com/']

folders = ['India','World','Business','Home']

functions = [get_articles_india,get_articles_world,get_articles_business,get_articles_home]

for i in range(4):
    make_folder(folders[i])
    names, data = functions[i](links[i],'./'+folders[i])
    for j,k in zip(names, data):
        create_file(j,k)
