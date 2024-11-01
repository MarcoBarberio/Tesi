class Node:
    def __init__(self,url,depth,father,resource_name,similarity):
        self.url=url
        self.depth=depth
        self.father=father
        self.resource_name=resource_name
        self.similarity=similarity
        if father:
            self.father.add_child(self)
    def to_string(self):
        return str(self.depth)+": "+self.url+ " similarity: "+str(self.similarity)
            
    def bfs(self):
        queue=[self]
        while queue:
            node=queue.pop(0)
            if isinstance(node, URL_node):
                print("URL "+str(node.depth)+": "+node.url)
                queue.extend(node.children)
            else:
                print(node.extension+" "+str(node.depth)+": "+node.url)
                
class URL_node(Node):
    def __init__(self,url,depth,father,resource_name,similarity):
        super().__init__(url,depth,father,resource_name,similarity)
        self.children=[]
    def add_child(self,child):
        if child:
            self.children.append(child)
    def print_data(self):
        print("URL "+super().to_string())
        
class File_node(Node):
    def __init__(self,url,depth,father,extension,resource_name,similarity):
        super().__init__(url,depth,father,resource_name,similarity)
        self.extension=extension
    def print_data(self):
        print(self.extension+" "+super().to_string())
    