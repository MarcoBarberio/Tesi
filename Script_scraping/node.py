#Ogni nodo contiene informazioni relative ad una pagina URL o un file
class Node:
    def __init__(self,url,depth,father,resource_name,similarity):
        self.url=url
        self.depth=depth
        self.father=father
        self.resource_name=resource_name
        self.similarity=similarity #Grado di similarità con i bilanci di similarità. Più è vicino ad 1, maggiore è la probabilità che contenga informazioni sui bilanci
        if father:
            self.father.add_child(self)
    
    def to_string(self):
        return str(self.depth)+": "+self.url+ " similarity: "+str(self.similarity)
            
    
class URL_node(Node):
    def __init__(self,url,depth,father,resource_name,similarity):
        super().__init__(url,depth,father,resource_name,similarity)
        self.children=[]
    def __add_child(self,child):
        if child:
            self.children.append(child)
    def print_data(self):
        print("URL "+super().to_string())
        
class File_node(Node):
    def __init__(self,url,depth,father,extension,resource_name,similarity):
        super().__init__(url,depth,father,resource_name,similarity)
        self.extension=extension.upper()
    def print_data(self):
        print(self.extension+" "+super().to_string())
    