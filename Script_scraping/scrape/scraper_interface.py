from abc import ABC, abstractmethod
#interfaccia per creare oggetti che facciano lo scrape di una singola pagina web
class Scraper_interface(ABC):
    @abstractmethod
    # restituisce informazioni da una pagina (le informazioni dipendono dall'implementazione)
    def get_data(self,url):
        pass
    


    