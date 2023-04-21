import re

import bs4
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup


class TheThao247(CrawlSpider):
	name = 'the-thao-247'
	start_urls = ['https://thethao247.vn/']
	allowed_domains = ['thethao247.vn']
	rules = [
		Rule(LinkExtractor(allow=""), callback='parse', follow=True),
	]

	def parse(self, response):
		if response.css('h1#title_detail::text').extract_first() is None:
			return

		title = response.css('h1#title_detail::text').extract_first().strip()
		url = response.url
		summary = response.css('p.sapo_detail::text').extract_first().strip()

		soup = bs4.BeautifulSoup(response.body, 'html.parser')
		paras = soup.select_one('div#content_detail').select('p')[1:]
		content = '\n\n'.join([p.get_text(strip=True) for p in paras])

		extra_metadata = {}
		time = response.css('div.time::text').extract_first().strip()
		extra_metadata['time'] = time
		extra_metadata['author'] = ''
		extra_metadata['tags'] = []

		# clean
		summary = re.sub('\n{3,}', '\n\n', summary)
		content = re.sub('\n{3,}', '\n\n', content)

		yield {
			"title": title,
			"url": url,
			"summary": summary,
			"content": content,
			"extra_metadata": extra_metadata
		}