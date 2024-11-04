import random
from urllib.parse import urlparse

extensions= (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx")

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

def get_extensions():
   return extensions

def get_file_extension(file):
    return file.split("/")[-1]

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
