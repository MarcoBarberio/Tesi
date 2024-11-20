from abc import ABC, abstractmethod
class Text_classificator_interface(ABC):
    @abstractmethod
    def get_prediction(self,text): 
        #restituisce il valore della predizione di una parola.
        pass
    