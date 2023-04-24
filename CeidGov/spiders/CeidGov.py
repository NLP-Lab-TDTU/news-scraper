from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class CeidGov(CrawlSpider):
	name = 'ceid-gov'
	allowed_domains = ['ceid.gov.vn']
	start_urls = ['https://ceid.gov.vn/']
	rules = (
		Rule(LinkExtractor(allow=''), follow=True, callback='parse'),
	)

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('h1.post-title') is None:
			return

		title = soup.select_one('h1.post-title').get_text(strip=True)
		time = soup.select_one('time.value-title').get_text(strip=True)
		summary = ''
		content_div = soup.select_one('div.post-content.description ')
		paragraphs = content_div.select('p')[:-1]
		author = content_div.select('p')[-1].get_text(strip=True)
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
