# -*- coding: utf-8 -*-
# Exemple : scrapy crawl webcrawlerbasic -a domain=domain.com -o sortie.json
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin
from tldextract import extract

class WebCrawlerBasic(CrawlSpider):
    name = 'webcrawlerbasic'
    #handle_httpstatus_list = [404,410,301,500]
    custom_settings = {'HTTPERROR_ALLOW_ALL': True}
    
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
        super(WebCrawlerBasic, self).__init__(*args, **kwargs)
        
    def parse_page(self, response):
        page = {'url': response.url, 'status': response.status}
        url_extracted = extract(response.url)
        if self.target_domain == "{}.{}".format(url_extracted.domain, url_extracted.suffix):
            page['links'] = self.parse_links(response)
        yield page
            
    def parse_links(self, response):
        links = {}
        links['internal'] = []
        links['external'] = []
        for link in response.css('a::attr(href)').getall():
            link = urljoin(self.start_urls[0], link)
            link_extracted = extract(link)
            if self.target_domain == "{}.{}".format(link_extracted.domain, link_extracted.suffix):
                links['internal'].append(link)
            else:
                links['external'].append(link)
        return links
            