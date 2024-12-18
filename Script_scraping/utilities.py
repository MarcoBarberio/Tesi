import random
from urllib.parse import urlparse
import re
import fitz
import requests
import os
from dotenv import load_dotenv
load_dotenv()

#si accede ad ogni pagina con un user agent diverso per evitare problemi di ban
def get_random_user_agent(): 
    user_agents = os.getenv("USER_AGENTS").split("-")
    return random.choice(user_agents)

def get_domain(url):
    #restituisce il dominio di una pagina
    return urlparse(url).netloc 

def get_resource_name(url):
    #restituisce il nome della risorsa (il nome della pagina o il nome del file senza estensione)
    resource=url.split("/")[-1].lower()
    if resource.endswith(os.getenv("EXTENSIONS")):
        return resource.split(".")[0]
    return resource

def get_extensions():
   return os.getenv("EXTENSIONS")

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


def pdf_to_txt(file):
    #restituisce il testo di un pdf
    txt_path=file.replace(file.split(".")[-1],"txt")
    try:
        with fitz.open(file) as pdf_document:
            with open(txt_path,"w",encoding="utf-8") as txt_file: 
                for page_num in range(len(pdf_document)):
                    text = pdf_document[page_num].get_text()
                    txt_file.write(text+"\n")
            return txt_path
    except Exception:
        return None

def get_pdf_text(file):
    #restituisce il testo di un pdf
    try:
        text=""
        with fitz.open(file) as pdf_document:
            for page_num in range(len(pdf_document)):
                    text+= pdf_document[page_num].get_text()+"\n"
        return text
    except Exception:
        return None
    
def download_pdf(file_url): 
    #scarica un file pdf
    try:
        # Effettua la richiesta HTTP per scaricare il PDF
        response = requests.get(file_url, stream=True)
        response.raise_for_status()  
        
        file_name = file_url.split("/")[-1]
        # Percorso completo del file di destinazione
        file_path = os.path.join(os.getenv("TMP_DIR"), file_name)
        
        # Salva il file in modalità binaria
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        return file_path
    except Exception as e:
        print(f"Errore durante il download di {file_url}: {e}")
        return None
    
def clean_tmp():
    tmp=os.getenv("TMP_DIR")
    for file_name in os.listdir(tmp):
        file=os.path.join(tmp,file_name)
        os.remove(file)
