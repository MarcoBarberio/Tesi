from node import URL_node,File_node
from scraper import get_links

def worker(max_depth,node_to_parse_queue,set_links,set_files,lock,parsed_node_queue):
    while(True):
        node=node_to_parse_queue.get()
        if node is None:
            node_to_parse_queue.task_done()
            break
        if node.depth>max_depth:
            node_to_parse_queue.task_done()
            continue
        
        links=get_links(node.url)
        if links["status_code"]!=200:
            node_to_parse_queue.task_done()
            parsed_node_queue.append(node)
            continue
        
        if not node.father:
            try:
                first_node=parsed_node_queue[0]
                parsed_node_queue[0]=node
                parsed_node_queue.append(first_node) #mi assicuro che il primo nodo sia effettivamente la radice
            except IndexError:
                ""    
        parsed_node_queue.append(node)

        
        for link in links["redirect_links"]:
            with lock:
                if link not in set_links:
                    if node.depth+1 <= max_depth:
                        set_links.add(link)                     
                        new_node=URL_node(link,node.depth+1,node)
                        node_to_parse_queue.put(new_node)
        for file in links["files"]:
            with lock:
                if file not in set_files:
                    extension=file.split(".")[-1].upper()
                    set_files.add(file)
                    new_node=File_node(file,node.depth+1,node,extension)
                    parsed_node_queue.append(new_node) 
        
        node_to_parse_queue.task_done()
