import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import MonetaItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class MonetaSpider(scrapy.Spider):
	name = 'moneta'
	start_urls = ['https://www.moneta.cz/blog']

	def parse(self, response):
		categories = response.xpath('//ul[@class="nav navbar-blank navbar-nav navbar-site"]/li/a/@href').getall()
		yield from response.follow_all(categories, self.post)

	def post(self, response):
		post_links = response.xpath('//a[@class="springboard-tile__heading-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		category = response.xpath('//div[@class="blog-article__content"]//text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="blog-article__content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=MonetaItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('category', category)

		yield item.load_item()
