# -*- coding: utf-8 -*-
# Exemple : scrapy crawl webcrawler -a domain=domain.com -o sortie.json
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin
from tldextract import extract

from WebCrawler.items import PageItems, LinksItems

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
        super(WebCrawler, self).__init__(*args, **kwargs)
        
    def parse_page(self, response):
        item = PageItems()
        item['url'] = response.url
        item['status'] = response.status
        url_extracted = extract(response.url)
        if self.target_domain == '{}.{}'.format(url_extracted.domain, url_extracted.suffix):
            item['links'] = self.parse_links(response)
        yield item
            
    def parse_links(self, response):
        item = LinksItems()
        item['internal'] = []
        item['external'] = []
        for link in response.css('a::attr(href)').getall():
            link = urljoin(self.start_urls[0], link)
            link_extracted = extract(link)
            if self.target_domain == '{}.{}'.format(link_extracted.domain, link_extracted.suffix):
                item['internal'].append(link)
            else:
                item['external'].append(link)
        return item
            