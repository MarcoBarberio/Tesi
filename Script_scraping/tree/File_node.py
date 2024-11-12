from .node import NodeInterface

# Nodo che contiene le informazioni di un file
class File_node(NodeInterface):
    def __init__(self, url, depth, father, resource_name, similarity, extension):
        self.__url = url
        self.__depth = depth
        self.__father = father
        self.__resource_name = resource_name
        self.__similarity = similarity
        self.__extension = extension
        if self.__father:
            self.__father.add_child(self)

    @property
    def url(self):
        return self.__url

    @property
    def depth(self):
        return self.__depth

    @property
    def father(self):
        return self.__father

    @property
    def resource_name(self):
        return self.__resource_name

    @property
    def similarity(self):
        return self.__similarity
    
    @property
    def extension(self):
        return self.__extension

    def to_string(self):
        return self.extension.upper()+" "+str(self.depth)+": "+self.url+ " similarity: "+str(self.similarity)