from .crawler_interface import Crawler_interface
from utilities import get_resource_name,is_valid_url,download_pdf,get_pdf_text,clean_tmp
from tree.URL_node import URL_node
from queue import Queue
import threading
from .worker import worker
from IA_models.text_classificator import Text_classicator

PREDICTION_THRESHOLD=0.20
#Data una pagina, si fa lo scrape fino ad un livello fissato
class Crawler(Crawler_interface):
    def __init__(self):
        self.__n_threads=30
        #grado di similarità sotto il quale si scartano i link raggiungibili da una pagina
        
        
    def crawl(self,root_url,max_depth,url_threshold,file_threshold):
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
        
        for i in range(self.__n_threads):
            thread=threading.Thread(target=worker,args=(max_depth,visited_url,visited_file,url_queue,file_queue,lock,url_threshold,file_threshold))
            #ogni thread naviga una pagina e ne estrae i link
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
        
        # filtro ulteriore eseguito da un text classificator per eliminare ulteriori pdf non consoni
        text_classifcator=Text_classicator()
        for file in file_queue:
            if file.extension != "pdf":
                continue
            prediction = text_classifcator.get_prediction_from_file(file.url)
            if prediction>PREDICTION_THRESHOLD:
                file_queue.remove(file)
        return file_queue
    