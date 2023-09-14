# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from WebCrawler.spiders.webcrawler import WebCrawler
import sqlite3


if __name__ == "__main__": 
    
    print("=== WELCOME TO WEBCRAWLER ===")
    print("About WebCrawler: https://github.com/thomasgottvalles/WebCrawler \n")
    domain = input("Enter the first website domain the robot will crawl: ")
    process = CrawlerProcess()
    process.crawl(WebCrawler, domain=domain)
    process.start()
    con = sqlite3.connect('demo.db')
    cur = con.cursor()
    
    while True:
        cur.execute("SELECT domain FROM sites WHERE status=0 ORDER BY id LIMIT 1 ")
        domain = cur.fetchone()[0]
        con.commit()
        print("\nNext website domain the robot will crawl: " + domain)
        case = input("What do you want to do ? crawl, jump, exit: ")
        if case == "crawl":
            command = "scrapy crawl webcrawler -a domain=" + domain
            subprocess.run(command, shell=True)
        if case == "jump":
            cur.execute("UPDATE sites SET status=1 WHERE domain='" + domain + "'")
            con.commit()
        if case == "exit":
            break