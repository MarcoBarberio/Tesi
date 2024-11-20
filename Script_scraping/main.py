from datetime import datetime
from hugchat import hugchat
from hugchat.login import Login
import os
from crawler.crawler import Crawler
from IA_models.text_generation import Text_generator
from scrape.scraper import Scraper
import requests
from utilities import download_pdf,get_pdf_text
from tensorflow.keras.models import load_model
import tensorflow as tf

if __name__=="__main__":
    
    
    x=datetime.now()
    url=input("Url: ")
    depth=int(input("Depth: "))
    crawler=Crawler()
    files=crawler.crawl(url,depth)
    if not files:
        files=crawler.crawl(url,depth+1)
    diff=datetime.now()-x
    total_seconds = diff.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    
    print("Profondità "+str(depth)+": "+str(minutes)+" min "+str(seconds)+"s")
    print("------------------------")
    for file in files:
        break

