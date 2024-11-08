from utilities import get_resource_name,is_valid_url
from node import URL_node
from datetime import datetime
from queue import Queue
import threading
from worker import worker
from scraper import get_links
n_threads=30
def crawl(root_url,max_depth):
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
    return file_queue

if __name__=="__main__":
    x=datetime.now()
    url=input("Url: ")
    depth=int(input("Depth: "))
    files=crawl(url,depth)
    diff=datetime.now()-x
    total_seconds = diff.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    
    print("Profondità "+str(depth)+": "+str(minutes)+" min "+str(seconds)+"s")
    print("------------------------")
    for file in files:
        file.print_data()