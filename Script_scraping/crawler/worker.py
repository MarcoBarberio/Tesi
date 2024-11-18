from tree.URL_node import URL_node
from tree.File_node import File_node
from scrape.scraper import Scraper
from utilities import get_resource_name,get_file_extension,get_clean_url
from queue import Empty
from IA_models.text_embedding import Text_embedder

#grado di similarità sotto il quale si scartano i link raggiungibili da una pagina
URL_similarity_threshold=-1
file_similarity_threshold=-1
def worker(max_depth,visited_url,visited_file,url_queue,file_queue,lock):
    #modello per calcolare la similarità tra le parole
    model=Text_embedder()
    scraper=Scraper()

    while True:
        try:
            node = url_queue.get()
        except Empty:
            continue
        #segnale di chiusura del thread
        if node is None: 
            url_queue.task_done()
            break
        if node.depth>=max_depth:
            url_queue.task_done()
            continue
        #restituisce tutti i link raggiungibili dalla pagina corrente
        links=scraper.get_data(node.url) 
        #se lo status code non è 200 c'è stato un errore nel reperimento di una pagina
        if not links:
            url_queue.task_done()
            continue
        if links["status_code"]!=200: 
            url_queue.task_done()
            continue
        #link è l'url completo contenuto nel campo href,text il campo testuale contenuto nell'anchor 
        #parent un insieme di parole casuale contenute nel contenitore dell'anchor,same_domain indica se il link appartiene allo stesso dominio del padre
        for link,text,parent,same_domain in links["redirect_links"]:
            with lock:                  
                #visited_url contiene i link già visitati e il suo accesso deve avvenire in mutua esclusione                
                if link in visited_url: 
                    continue
                visited_url.add(link)
                
            resource_name=get_resource_name(link)
            clean_link=get_clean_url(link)
            #la parola di cui ottenere la similarità è un insieme di link,text e parent
            similarity=model.get_similarity(clean_link+","+text+","+parent)
            #se l'url non è contenuto nello stesso dominio del padre si filtra abbassando la similarità
            if not same_domain:
                similarity-=0.1
            #Se la similarità è maggiore della soglia si crea un nodo che contiene le informazioni della pagina
            if similarity>URL_similarity_threshold:
                new_node=URL_node(link,node.depth+1,node,resource_name,similarity)
                print(new_node.to_string())
                url_queue.put(new_node)
        #stessa procedura ma con i file
        for file,text,parent,same_domain in links["files"]:
            with lock:
                if file in visited_file:
                    continue
                visited_file.add(file)
            resource_name=get_resource_name(file)
            clean_file_name=get_clean_url(file)
            similarity=model.get_similarity(clean_file_name+","+text+","+parent)
            if not same_domain:
                similarity-=0.1
            if similarity>file_similarity_threshold:
                new_node=File_node(file,node.depth+1,node,resource_name,similarity,get_file_extension(file))
                print(new_node.to_string())
                file_queue.append(new_node)    
        url_queue.task_done()
    
