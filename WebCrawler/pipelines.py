# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class WebCrawlerPipeline:
    def __init__(self):

        ## Create/Connect to database
        self.con = sqlite3.connect('demo.db')

        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS pages(
            url TEXT,
            status INT,
            links_external TEXT,
            links_internal TEXT
        )
        """)
        
    def process_item(self, item, spider):
        item.setdefault('links', {})
        item['links'].setdefault('external',  [])
        item['links'].setdefault('internal', [])
  
        ## Define insert statement
        self.cur.execute("""
            INSERT INTO pages (url, status, links_external, links_internal) VALUES (?, ?, ?, ?)
        """,
        (
            item['url'],
            item['status'],
            str(item['links']['external']),
            str(item['links']['internal'])
        ))
        
        ## Execute insert of data into database
        self.con.commit()
        return item
