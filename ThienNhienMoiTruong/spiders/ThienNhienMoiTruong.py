from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class ThienNhienMoiTruong(CrawlSpider):
	name = 'tn-mt'
	allowed_domains = ['thiennhienmoitruong.vn']
	start_urls = ['https://thiennhienmoitruong.vn/']
	rules = (
		Rule(LinkExtractor(allow=''), follow=True, callback='parse'),
	)

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('h1.title-pr') is None:
			return

		title = soup.select_one('h1.title-pr').get_text(strip=True)
		time = soup.select_one('p.date').get_text(strip=True)
		content_div = soup.select_one('div.content-content')
		summary = content_div.select_one('p').get_text(strip=True)
		paragraphs = content_div.select('p')[1:]
		author = ''
		texts = [p.get_text(strip=True) for p in paragraphs if p is not None]
		content = '\n\n'.join([p for p in texts if p != ''])

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
