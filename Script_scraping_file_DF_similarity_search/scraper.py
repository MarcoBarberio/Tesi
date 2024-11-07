from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import requests
from utilities import get_random_user_agent,get_domain,get_random_words,get_extensions
from urllib.parse import urljoin
import time
from selenium.webdriver.common.by import By  
import undetected_chromedriver as uc
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
    
    response = requests.get(url,headers={"User-Agent":get_random_user_agent()})
    markup=response.text
    if response.status_code != 200:
        if response.status_code==403:
            dynamic_search(url,link_dict)
            response.status_code=200
        else:
            print("Errore "+str(response.status_code)+" nel caricamento della pagina "+url)
            link_dict["status_code"]=response.status_code
            return link_dict
            
    link_dict["status_code"]=response.status_code
    
    soup = BeautifulSoup(markup, 'html.parser')
    
    static_search(soup,url,link_dict)
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
            link_dict["redirect_links"].append((full_url,text,parent))


def dynamic_search(url,link_dict):
    domain = get_domain(url)
    driver=get_driver(url)
    driver.get(url)
    links=driver.find_elements(By.TAG_NAME,"a")
    
    if links[0].text=="Cloudflare": #si prova con uc per evitare il blocco
        try:
            driver.quit()
        except OSError:
            ""
        driver_uc=uc.Chrome(headless=False,use_subprocess=True)
        driver_uc.get(url)
        links=driver_uc.find_elements(By.TAG_NAME,"a")
        for link in links:
            switch_link(link,url,domain,link_dict)
        try:
            driver_uc.quit()
        except OSError:
            ""
    else:
        for link in links:
            switch_link(link,url,domain,link_dict)
        try:
            driver.quit()
        except OSError:
            ""

def switch_link(link,url,domain,link_dict):
    href = link.get_attribute("href")
    text=link.text
    link_parent=link.find_element(By.XPATH, "..").text
    parent=""
    if link_parent is not None:
        parent=get_random_words(link_parent)
        
    full_url = urljoin(url, href) 
    if full_url == url:
        return      
    full_url_domain = get_domain(full_url)
    if full_url_domain != domain:
        return
    if full_url.lower().endswith(get_extensions()):
        link_dict["files"].append((full_url,text,parent))
    else:
        link_dict["redirect_links"].append((full_url,text,parent))