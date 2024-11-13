from abc import ABC, abstractmethod
class Text_embedder_interface(ABC):
    @abstractmethod
    def _create_dictionary_embeddings(self): 
        #crea un json contenente gli embeddings delle parole contenute nel dizionario 
        pass
    
    def _get_embedding(self,word):
        #data una parola restituisce il suo embedding
        pass
    
    def get_similarity(self,word):
        #data una parola restituisce la similarità con il dizionario
        pass