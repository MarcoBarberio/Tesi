import random
from urllib.parse import urlparse
import re
extensions= (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx")

#si accede ad ogni pagina con un user agent diverso per evitare problemi di ban
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
    #restituisce il dominio di una pagina
    return urlparse(url).netloc 

def get_resource_name(url):
    #restituisce il nome della risorsa (il nome della pagina o il nome del file senza estensione)
    resource=url.split("/")[-1].lower()
    if resource.endswith(extensions):
        return resource.split(".")[0]
    return resource

def get_extensions():
   return extensions

def get_file_extension(file):
    #restituisce l'estensione di un file
    return file.split("/")[-1].split(".")[-1]

def is_valid_url(url): 
    #verifica la validità di un url
    parsed_url=urlparse(url)
    return all([parsed_url.scheme,parsed_url.netloc])

def get_random_words(text):
    #restituisce un insieme di parole casuali di un insieme di parole
    words=text.split()
    n=random.randint(10,20)
    if(n>len(words)):
        return text
    words=random.sample(words,n)
    result_text=""
    for word in words:
        result_text+=" "+word
    return result_text

def get_clean_url(url): 
    #dato un link lo rende più leggibile per il modello di text embedding
    return re.sub(r"[\/%/-/_/\d]"," ",url)

    