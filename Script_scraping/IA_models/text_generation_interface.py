from abc import ABC, abstractmethod
class Text_generator_interface(ABC):
    @abstractmethod
    def query(self,prompt):
        # restituisce il risultato dell'interrogazione all'ia dato un prompt
        pass