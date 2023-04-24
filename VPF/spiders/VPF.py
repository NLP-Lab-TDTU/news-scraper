from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class VPF(CrawlSpider):
	name = 'vpf-tin-tuc'
	start_urls = [
		'https://vpf.vn/tin-tuc/']
	allowed_domains = ['vpf.vn']
	rules = [
		Rule(LinkExtractor(allow='/tin-tuc/'), follow=True, callback='parse')
	]

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('h1.entry-title') is None:
			return

		title = soup.select_one('h1.entry-title').get_text(strip=True)
		author = ''
		time = ''
		summary = ''
		content_div = soup.select_one('div.td-post-content')
		paragraphs = content_div.select('p')
		content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
		extra_metadata = {'time': time, 'author': author, 'tags': []}

		# clean
		summary = re.sub('\n{3,}', '\n\n', summary)
		content = re.sub('\n{3,}', '\n\n', content)

		yield {
			'title': title,
			'url': response.url,
			'summary': summary,
			'content': content,
			'extra_metadata': extra_metadata
		}
