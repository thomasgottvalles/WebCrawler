# -*- coding: utf-8 -*-
# Exemple : scrapy crawl webcrawler -a url=domain.com -o sortie.xml
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin
from tldextract import extract

class WebCrawler(CrawlSpider):
    name = 'webcrawler'
    handle_httpstatus_list = [404,410,301,500]
    
    def __init__(self, url=None, *args, **kwargs):
        self.start_urls = ['https://' + url]
        self.target_domain = url
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
        page = {'URL':response.url, 'Status':response.status}
        extracted = extract(response.url)
        if self.target_domain == "{}.{}".format(extracted.domain, extracted.suffix):
            page['Links'] =  self.parse_links(response)
        yield page
            
    def parse_links(self, response):
        links = []
        for link in response.css('a::attr(href)').getall():
            links.append(urljoin(self.start_urls[0], link))
        return links
            