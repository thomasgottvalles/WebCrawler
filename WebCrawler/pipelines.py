# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from WebCrawler.items import PageItems, SiteItems
import sqlite3

class WebCrawlerPipeline:
    
    def __init__(self):
        self.site_id = 0
        self.con = sqlite3.connect('demo.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS sites(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT,
            status INT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS pages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site_id INT,
            url TEXT,
            status INT,
            links_external TEXT,
            links_internal TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
    def open_spider(self, spider):
        if self.cur.execute("SELECT 1 FROM sites WHERE domain='" + spider.target_domain + "'").fetchone():
            self.cur.execute("UPDATE sites SET status=1 WHERE domain='" + spider.target_domain + "'")
        else:
            self.cur.execute("INSERT INTO sites (domain, status) VALUES (?, ?)",
            (
                spider.target_domain,
                1
            ))
        self.cur.execute("SELECT id FROM sites WHERE domain='" + spider.target_domain + "'")
        self.site_id = self.cur.fetchone()[0]
        self.con.commit()
        
    def process_item(self, item, spider):
        if isinstance(item, SiteItems):
            if not self.cur.execute("SELECT 1 FROM sites WHERE domain='" + item['domain'] + "'").fetchone():
                self.cur.execute("INSERT INTO sites (domain, status) VALUES (?, ?)",
                (
                    item['domain'],
                    0
                ))
                self.con.commit()
        if isinstance(item, PageItems):
            item.setdefault('links', {})
            item['links'].setdefault('external', [])
            item['links'].setdefault('internal', [])
            self.cur.execute("INSERT INTO pages (site_id, url, status, links_external, links_internal) VALUES (?, ?, ?, ?, ?)",
            (
                self.site_id,
                item['url'],
                item['status'],
                str(item['links']['external']),
                str(item['links']['internal'])
            ))
            self.con.commit()
        return item
    
    def close_spider(self, spider):
        print("WebCrawlerPipeline/close_spider")
