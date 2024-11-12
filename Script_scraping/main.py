from datetime import datetime
from hugchat import hugchat
from hugchat.login import Login
import os
from scrape.crawler import Crawler

if __name__=="__main__":
    x=datetime.now()
    url=input("Url: ")
    depth=int(input("Depth: "))
    crawler=Crawler()
    files=crawler.crawl(url,depth)
    diff=datetime.now()-x
    total_seconds = diff.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    
    print("Profondità "+str(depth)+": "+str(minutes)+" min "+str(seconds)+"s")
    print("------------------------")
    for file in files:
        print(file.to_string())