class Node:
    def __init__(self,url,depth,father):
        self.url=url
        self.depth=depth
        self.father=father
        if father:
            self.father.add_child(self)
    def to_string(self):
        return str(self.depth)+": "+self.url
            
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
    def __init__(self,url,depth,father):
        super().__init__(url,depth,father)
        self.children=[]
    def add_child(self,child):
        if child:
            self.children.append(child)
    def print_data(self):
        print("URL "+super().to_string())
        
class File_node(Node):
    def __init__(self,url,depth,father,extension):
        super().__init__(url,depth,father)
        self.extension=extension
    def print_data(self):
        print(self.extension+" "+super().to_string())
    