# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
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
        self.cur.execute("""
            INSERT INTO sites (domain) VALUES (?)
        """,
        (
            spider.target_domain,
        ))
       
        self.cur.execute("""SELECT id FROM sites ORDER BY id DESC LIMIT 1""")
        self.site_id = self.cur.fetchone()[0]
        self.con.commit()
        
    def process_item(self, item, spider):
        item.setdefault('links', {})
        item['links'].setdefault('external',  [])
        item['links'].setdefault('internal', [])
        self.cur.execute("""
            INSERT INTO pages (site_id, url, status, links_external, links_internal) VALUES (?, ?, ?, ?, ?)
        """,
        (
            self.site_id,
            item['url'],
            item['status'],
            str(item['links']['external']),
            str(item['links']['internal'])
        ))
        self.con.commit()
        return item
