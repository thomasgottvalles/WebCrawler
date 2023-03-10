# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from WebCrawler.spiders.webcrawler import WebCrawler
import sqlite3
import subprocess


if __name__ == "__main__": 
    
    domain = input("Enter the first website domain the robot will crawl:")
    process = CrawlerProcess()
    process.crawl(WebCrawler, domain=domain)
    process.start()
    con = sqlite3.connect('demo.db')
    cur = con.cursor()
    
    while True:
        cur.execute("SELECT domain FROM sites WHERE status=0 ORDER BY id LIMIT 1 ")
        domain = cur.fetchone()[0]
        con.commit()
        print("Next website domain the robot will crawl:" + domain)
        command = 'scrapy crawl webcrawler -a domain=' + domain
        subprocess.run(command, shell=True)