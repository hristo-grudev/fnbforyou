import scrapy

from scrapy.loader import ItemLoader

from ..items import FnbforyouItem
from itemloaders.processors import TakeFirst


class FnbforyouSpider(scrapy.Spider):
	name = 'fnbforyou'
	start_urls = ['https://www.fnbforyou.com/about/news/']

	def parse(self, response):
		post_links = response.xpath('//p[@class="action"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="main-content"]/p[position()>1]//text()[normalize-space() and not(ancestor::p[@class="action"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="main-content"]/p[1]/text()').get()

		item = ItemLoader(item=FnbforyouItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
