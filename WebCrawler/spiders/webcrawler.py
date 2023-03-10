# -*- coding: utf-8 -*-
# Exemple : scrapy crawl webcrawler -a domain=domain.com -o sortie.json
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin
from tldextract import extract

from WebCrawler.items import PageItems, LinksItems, SiteItems

from pydispatch import dispatcher
from scrapy import signals

class WebCrawler(CrawlSpider):
    name = 'webcrawler'
    #handle_httpstatus_list = [404,410,301,500]
    custom_settings = { 'HTTPERROR_ALLOW_ALL': True,
                        'ITEM_PIPELINES':{'WebCrawler.pipelines.WebCrawlerPipeline': 300}}

    def __init__(self, domain=None, *args, **kwargs):
        self.start_urls = ['http://' + domain]
        self.target_domain = domain
        self.rules = [
            Rule(
                LinkExtractor(allow_domains=self.target_domain), 
                callback='parse_page',
                follow=True),
            Rule(
                callback='parse_page')
        ]
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dispatcher.connect(self.spider_idle, signals.spider_idle)
        super(WebCrawler, self).__init__(*args, **kwargs)
        
    def parse_page(self, response):
        item_page = PageItems()
        item_page['url'] = response.url
        item_page['status'] = response.status
        url_extracted = extract(response.url)
        if self.target_domain == '{}.{}'.format(url_extracted.domain, url_extracted.suffix):
            item_page['links'] = self.parse_links(response)
        else:
            item_site = SiteItems()
            item_site['domain'] = '{}.{}'.format(url_extracted.domain, url_extracted.suffix)
            yield item_site
        yield item_page    
                
    def parse_links(self, response):
        item_links = LinksItems()
        item_links['internal'] = []
        item_links['external'] = []
        for link in response.css('a::attr(href)').getall():
            link = urljoin(self.start_urls[0], link)
            link_extracted = extract(link)
            if self.target_domain == '{}.{}'.format(link_extracted.domain, link_extracted.suffix):
                item_links['internal'].append(link)
            else:
                item_links['external'].append(link)
        return item_links
    
    def spider_opened(self):
        print("WebCrawler/spider_opened")
        
    def spider_idle(self):
        print("WebCrawler/spider_idle")     
    
    def spider_closed(self):
        print("WebCrawler/spider_closed")