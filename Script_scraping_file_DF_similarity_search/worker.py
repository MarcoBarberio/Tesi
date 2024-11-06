from node import URL_node,File_node
from scraper import get_links
from utilities import get_resource_name,get_file_extension,get_clean_url
from queue import Empty
from model import Model
similarity_threshold=0.3
def worker(max_depth,visited_url,url_queue,file_queue,lock):
    model=Model()
    while(True):
        try:
            node = url_queue.get()
        except Empty:
            continue
        if node is None:
            url_queue.task_done()
            break
        if node.depth>=max_depth:
            url_queue.task_done()
            continue
        links=get_links(node.url)
        if links["status_code"]!=200:
            url_queue.task_done()
            continue
        print(node.url+": "+str(node.similarity))
        for link,text,parent in links["redirect_links"]:
            with lock:
                if link in visited_url:
                    continue
                visited_url.add(link)
            resource_name=get_resource_name(link)
            clean_link=get_clean_url(link)
            similarity=model.get_similarity(clean_link+","+text+","+parent)
            if similarity>similarity_threshold:
                new_node=URL_node(link,node.depth+1,node,resource_name,similarity)
                new_node.print_data()
                url_queue.put(new_node)
        for file,text,parent in links["files"]:
            resource_name=get_resource_name(file)
            clean_file_name=get_clean_url(file)
            similarity=model.get_similarity(clean_file_name+","+text+","+parent)
            if similarity>similarity_threshold:
                new_node=File_node(file,node.depth+1,node,get_file_extension(file),resource_name,similarity)
                new_node.print_data()
                file_queue.append(new_node)    
        url_queue.task_done()
