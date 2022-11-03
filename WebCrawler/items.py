# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PageItems(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    links = scrapy.Field()
    pass

class LinksItems(scrapy.Item):
    external = scrapy.Field()
    internal = scrapy.Field()
    pass
