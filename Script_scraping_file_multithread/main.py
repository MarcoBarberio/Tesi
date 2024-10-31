from scraper import is_valid_url
from node import URL_node
from worker import worker
from queue import Queue
import threading
from datetime import datetime

def crawl(url,max_depth):
    if not is_valid_url(url):
        print("Url non valido")
        return
    
    node_to_parse_queue=Queue()
    set_links=set()
    set_files=set()
    parsed_node_queue=[]
    lock=threading.Lock()
    num_threads=10
    threads=[]
    
    first_node=URL_node(url,0,None)
    node_to_parse_queue.put(first_node)
    for i in range(num_threads):
        thread=threading.Thread(target=worker,args=(max_depth,node_to_parse_queue,set_links,set_files,lock,parsed_node_queue))
        thread.start()
        threads.append(thread)
    
    node_to_parse_queue.join()
    for thread in threads:
        node_to_parse_queue.put(None)
    for thread in threads:
        thread.join()
        i=0
    for node in parsed_node_queue:
        i=i+1
        node.print_data()
    print(i)

if __name__=="__main__":
    depth=3
    x=datetime.now()
    crawl("https://www.efrag.org/en",depth)
    diff=datetime.now()-x
    total_seconds = diff.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    print("Profondità "+str(depth)+": "+str(minutes)+" min "+str(seconds)+"s")