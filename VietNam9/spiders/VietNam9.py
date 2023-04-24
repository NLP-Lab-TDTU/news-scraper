from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class VietNam9(CrawlSpider):
	name = 'viet-nam-9'
	start_urls = [
		'https://vietnam9.net/']
	allowed_domains = ['vietnam9.net']
	rules = [
		Rule(LinkExtractor(allow=''), follow=True, callback='parse')
	]

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('h1.post-title') is None:
			return

		title = soup.select_one('h1.post-title').get_text(strip=True)

		author = ''
		_author = soup.select_one('a.author-name')
		if _author:
			author = _author.get_text(strip=True)

		time = ''
		summary = ''
		content_div = soup.select_one('div.entry-content')
		paragraphs = content_div.select('p, h1, h2, h3')
		content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p])

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
