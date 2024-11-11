from utilities import get_resource_name,is_valid_url,get_clean_url
from node import URL_node
from datetime import datetime
from queue import Queue
import threading
from worker import worker
from hugchat import hugchat
from hugchat.login import Login
import os
import re

n_threads=30
def crawl(root_url,max_depth,chatbot):
    if not is_valid_url(root_url):
        return
    
    root_resource_name=get_resource_name(root_url)
    root=URL_node(root_url,0,None,root_resource_name,0)
    #Coda che contiene le pagine web da cui prendere le informazioni. Queue è threadsafe
    url_queue=Queue() 
    url_queue.put(root)
    #Array di file che contengono preferibilmente bilanci di sosteniblità
    file_queue=[] 
    visited_url=set()
    visited_file=set()
    lock=threading.Lock()
    threads=[]
    
    for i in range(n_threads):
        thread=threading.Thread(target=worker,args=(max_depth,visited_url,visited_file,url_queue,file_queue,lock)) #ogni thread naviga una pagina e ne estrae i link
        thread.start()
        threads.append(thread)
    url_queue.join()
    #Segnale di terminazione dei thread
    for thread in threads:
        url_queue.put(None)
    #join dei thread
    for thread in threads:
        thread.join()
    file_queue.sort(key=lambda node: node.similarity, reverse=True)
    #interrogazione alla generative AI per filtrare file che non contengono bilanci di sostenibilità 
    query=""
    for file in file_queue:
        query+=get_clean_url(file.url)+"\n"
    message_result = str(chatbot.chat(query +" per ogni riga indicare se è un bilancio di sostenibilità o meno, rispondendo con y se lo è o con n altrimenti. non includere altro testo nella risposta"))
    #la risposta è si compone di una string iniziale seguita da una tabella con colonne: #riga. y/n
    print("----------------------")
    for file in file_queue:
        file.print_data()
    print(message_result)
    message_result = re.sub(r"\d+\.\s", "", message_result)
    responses=message_result.split("\n")
    indices_to_remove = [i for i, response in enumerate(responses) if response.strip().lower() == "n"]
    for index in reversed(indices_to_remove):
        del file_queue[index]
    print(len(file_queue))
    return file_queue

if __name__=="__main__":
    EMAIL = "mbarberio23@gmail.com"
    PASSWD = os.environ["PASSWORD_HUGGINGFACE"]
    cookie_path_dir = "./cookies/"
    sign = Login(EMAIL, PASSWD)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

# Create your ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    x=datetime.now()
    url=input("Url: ")
    depth=int(input("Depth: "))
    files=crawl(url,depth,chatbot)
    diff=datetime.now()-x
    total_seconds = diff.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    
    print("Profondità "+str(depth)+": "+str(minutes)+" min "+str(seconds)+"s")
    print("------------------------")
    for file in files:
        file.print_data()