import scrapy


class MonetaItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
    link = scrapy.Field()
