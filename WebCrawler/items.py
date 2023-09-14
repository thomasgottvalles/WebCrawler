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

class SiteItems(scrapy.Item):
    domain = scrapy.Field()
    pass
