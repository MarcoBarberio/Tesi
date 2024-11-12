from abc import ABC, abstractmethod
#interfaccia per creare oggetti che facciano lo scrape di una singola pagina web
class Scraper_interface(ABC):
    @abstractmethod
    # restituisce tutti i link e i file contenuti nella pagina
    def get_links(self,url):
        pass
    
    @abstractmethod
    # esegue uno scraping statico con beautiful soap
    #soup è un oggetto di tipo beautiful soap
    #link dict è un dizionario che contiene i link reindirizzabili dalla pagina, i file e il codice di stato della connessione
    def _static_search(self,url,soup,link_dict):
        pass
    
    @abstractmethod
    # esegue uno scraping dinamico con Selenium
    def _dynamic_search(self,url):
        pass

    @abstractmethod    
    # restituisce un driver di Selenium
    def _get_driver(self):
        pass
    