from abc import ABC, abstractmethod
#interfaccia per creare oggetti che facciano lo scrape di una singola pagina web
class Scraper_interface(ABC):
    @abstractmethod
    # restituisce informazioni da una pagina (le informazioni dipendono dall'implementazione)
    def get_data(self,url):
        pass
    
    @abstractmethod
    # esegue lo scraping di una pagina
    # data_dict è un dizionario che contiene le informazioni da restituire
    def _search(self,url,data_dict):
        pass

    
    