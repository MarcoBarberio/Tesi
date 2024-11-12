from abc import ABC, abstractmethod

class NodeInterface(ABC):
    @property
    @abstractmethod
    def url(self):
        # URL per reperire il nodo
        pass

    @property
    @abstractmethod
    def depth(self):
        # Profondità del nodo
        pass

    @property
    @abstractmethod
    def father(self):
        # Riferimento al nodo padre
        pass
    
    @property
    @abstractmethod
    def resource_name(self):
        # Nome della pagina o del file senza estensione
        pass

    @property
    @abstractmethod
    def similarity(self):
        # Grado di similarità con i bilanci di similarità
        pass

    @abstractmethod
    def to_string(self):
        # Restituisce una rappresentazione in stringa del nodo
        pass
