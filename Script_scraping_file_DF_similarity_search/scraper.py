from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import requests
from utilities import get_random_user_agent,get_domain,get_random_words,get_extensions
from urllib.parse import urljoin

#from ..gemini_lib import gemini_query

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
    #if check_dynamic_content(soup):
        #dynamic_search(url,link_dict)
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
        if full_url.lower().endswith(get_extensions()):
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
        if href.lower().endswith(get_extensions()):
            full_url=urljoin(url,href)
            link_dict["files"].append(full_url)
            
""" def ai_link_filter(url):
    query="L'url: "+url+''' potrebbe contenere file contenenti bilanci di sostenibilità, o altri link che portano a questi bilanci?
        Rispondi solo con Y/N'''
    response=gemini_query(query)
    return response=="Y" """
      
