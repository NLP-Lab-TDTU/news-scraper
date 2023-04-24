from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class ThanNong(CrawlSpider):
	name = 'tin-tuc-nn'
	start_urls = [
		'https://www.tintucnongnghiep.com/']
	allowed_domains = ['tintucnongnghiep.com']
	rules = [
		Rule(LinkExtractor(allow=''), follow=True, callback='parse')
	]

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('h1.post-title.entry-title') is None:
			return

		title = soup.select_one('h1.post-title.entry-title').get_text(strip=True)
		time = soup.select_one('p.post-meta abbr.timeago').get_text(strip=True)
		summary = ''
		content_div = soup.select_one('div.post-body')
		paragraphs = content_div.select('p')
		content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p is not None])
		tags = []

		tags_ = soup.select('p.post-tag a')
		tags = [a.get_text(strip=True) for a in tags_ if a is not None]
		tags = [t for t in tags if t != '']

		extra_metadata = {'time': time, 'author': '', 'tags': tags}

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
