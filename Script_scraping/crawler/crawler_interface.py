from abc import ABC, abstractmethod
# interfaccia per oggetti che si occupano di fare lo scrape di un sito
class Crawler_interface(ABC):
    @abstractmethod
    def crawl(url,max_depth):
        pass