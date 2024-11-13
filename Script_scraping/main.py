from datetime import datetime
from hugchat import hugchat
from hugchat.login import Login
import os
from scrape.crawler import Crawler
from IA_models.text_generation import Text_generator
if __name__=="__main__":
    generator=Text_generator()
    response=generator.query("""You're an expert in ESG.\n
                Given a set of links that contain PDF files, you need to identify which of these are sustainability reports.\n
                For each file, you should respond solely with "y" if it is a sustainability report or "n" otherwise.\n
                Here is the text:\n\n
                https://www.eni.com/content/dam/enicom/documents/ita/sostenibilita/2017/EniFor-2017-report.pdf \n
                https://www.eni.com/content/dam/enicom/documents/ita/sostenibilita/2018/EniFor-2018-report.pdf,""")
    print(response)
    """x=datetime.now()
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
        print(file.to_string())"""