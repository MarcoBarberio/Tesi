from scraper import get_links,get_resource_name,get_extension,is_valid_url
from similarity_search import get_similarity
import random
from node import File_node,URL_node
from datetime import datetime
def crawl(node,max_depth,visited_url):
    if node is None:
        return None
    if node.depth>=max_depth:
        return None
    links=get_links(node.url)
    if links["status_code"]!=200:
        return None
    print(node.url+": "+str(node.similarity))
    url_nodes=[]
    file_nodes=[]
    for link,text,parent in links["redirect_links"]:
        if link in visited_url:
            continue
        visited_url.append(link)
        resource_name=get_resource_name(link)
        similarity=get_similarity(link+","+text+","+parent)
        if similarity>0.09:
            new_node=URL_node(link,node.depth+1,node,resource_name,similarity)
            new_node.print_data()
            url_nodes.append(new_node)
    for file,text,parent in links["files"]:
        resource_name=get_resource_name(file)
        similarity=get_similarity(file+","+text+","+parent)
        if similarity>0.09:
            new_node=File_node(file,node.depth+1,node,get_extension(file),resource_name,similarity)
            new_node.print_data()
            file_nodes.append(new_node)    
    return (url_nodes,file_nodes)

def crawler(root_url,max_depth):
    if not is_valid_url(root_url):
        return
    
    root_resource_name=get_resource_name(root_url)
    root=URL_node(root_url,0,None,root_resource_name,0)
    url_queue=[root]
    file_queue=[]
    visited_url=[root]
    while url_queue:
        node=url_queue.pop() #nodo con priorità piu alta
        visited_url.append(node.url)
        links=crawl(node,max_depth,visited_url)
        if links is not None:
            url_queue.extend(links[0])
            file_queue.extend(links[1])
        url_queue.sort(key=lambda node: node.similarity)
    file_queue.sort(key=lambda node: node.similarity)
    return file_queue

if __name__=="__main__":
    depth=1
    x=datetime.now()
    crawler("https://www.efrag.org/en",depth)
    diff=datetime.now()-x
    total_seconds = diff.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    
    print("Profondità "+str(depth)+": "+str(minutes)+" min "+str(seconds)+"s")