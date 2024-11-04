from bs4 import BeautifulSoup
from urllib.parse import urlparse,urljoin
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import requests
import random
import time
#from ..gemini_lib import gemini_query
extensions= (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx")

def get_driver(url):
    options = Options()
    options.add_argument("--headless")
    driver = Chrome( options=options)   
    driver.get(url)
    return driver
    
def get_links(url):
    link_dict = {
        "redirect_links": [],
        "files": [],
        "status_code":0
    }
    
    response = requests.get(url,headers={"User_Agent":get_random_user_agent()})
    
    '''while response.status_code==429:
        time.sleep(5)
        response = requests.get(url,headers={"User_Agent":get_random_user_agent()}) #prova una seconda volta
    '''
    if response.status_code != 200:        
        print("Errore "+str(response.status_code)+" nel caricamento della pagina "+url)
        link_dict["status_code"]=response.status_code
        return link_dict
        
    link_dict["status_code"]=response.status_code
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    static_search(soup,url,link_dict)
    if check_dynamic_content(soup):
        #dynamic_search(url,link_dict)
        ""   
    return link_dict

def static_search(soup,url,link_dict):
    domain = get_domain(url)
    links=soup.find_all("a",href=True)
    for link in links:
        href = link.get("href")
        text=link.text
        link_parent=link.parent.text
        parent=""
        if link_parent is not None:
            parent=get_random_words(link_parent)
            
        full_url = urljoin(url, href) 
        if full_url == url:
            continue      
        full_url_domain = get_domain(full_url)
        if full_url_domain != domain:
            continue
        if full_url.lower().endswith(extensions):
                link_dict["files"].append((full_url,text,parent))
        else:
            #if ai_link_filter(full_url):
                link_dict["redirect_links"].append((full_url,text,parent))

def dynamic_search(url,link_dict):
    print("contenuti dinamici")
    driver=get_driver(url)
    driver.implicitly_wait(10)
    soup=BeautifulSoup(driver.page_source,"html_parser")
    driver.quit()
    
    for link in soup.find_all("a",href=True):
        href=link.get("href")
        if href.lower().endswith(extensions):
            full_url=urljoin(url,href)
            link_dict["files"].append(full_url)
            
""" def ai_link_filter(url):
    query="L'url: "+url+''' potrebbe contenere file contenenti bilanci di sostenibilità, o altri link che portano a questi bilanci?
        Rispondi solo con Y/N'''
    response=gemini_query(query)
    return response=="Y" """
      
def get_random_user_agent():
    user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36 Edge/12.10240"
    ]
    return random.choice(user_agents)
def get_domain(url):
    return urlparse(url).netloc

def get_resource_name(url):
    resource=url.split("/")[-1].lower()
    if resource.endswith(extensions):
        return resource.split(".")[0]
    return resource

def get_extension(url):
    extension=url.split(".")[-1].upper()
    return extension

def is_valid_url(url):
    parsed_url=urlparse(url)
    return all([parsed_url.scheme,parsed_url.netloc])

def check_dynamic_content(soup):
    return bool(soup.find_all("div",class_="dynamic_content"))

def get_random_words(text):
    words=text.split()
    n=random.randint(10,20)
    if(n>len(words)):
        return text
    words=random.sample(words,n)
    result_text=""
    for word in words:
        result_text+=" "+word
    return result_text