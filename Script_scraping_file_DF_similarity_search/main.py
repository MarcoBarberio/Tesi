from utilities import get_resource_name,is_valid_url
from node import URL_node
from datetime import datetime
from queue import Queue
import threading
from worker import worker
from scraper import get_links
n_threads=10
def crawl(root_url,max_depth):
    if not is_valid_url(root_url):
        return
    
    root_resource_name=get_resource_name(root_url)
    root=URL_node(root_url,0,None,root_resource_name,0)
    url_queue=Queue() #Coda che contiene le pagine web da cui prendere le informazioni. Queue è threadsafe
    url_queue.put(root)
    file_queue=[] #Array di file che contengono preferibilmente bilanci di sosteniblità
    visited_url=set()
    lock=threading.Lock()
    threads=[]
    
    for i in range(n_threads):
        thread=threading.Thread(target=worker,args=(max_depth,visited_url,url_queue,file_queue,lock)) #ogni thread naviga una pagina e ne estrae i link
        thread.start()
        threads.append(thread)
    url_queue.join()
    for thread in threads:
        url_queue.put(None)
    for thread in threads:
        thread.join()
    file_queue.sort(key=lambda node: node.similarity)
    return file_queue

if __name__=="__main__":
    #get_links("https://www.sofidel.com/")
    depth=1
    x=datetime.now()
    crawl("https://www.efrag.org/en",depth)
    diff=datetime.now()-x
    total_seconds = diff.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    
    print("Profondità "+str(depth)+": "+str(minutes)+" min "+str(seconds)+"s")
    