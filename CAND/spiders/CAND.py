from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class CAND(CrawlSpider):
	name = 'cand'
	allowed_domains = ['cand.com.vn']
	start_urls = ['https://cand.com.vn/']
	rules = (
		Rule(LinkExtractor(allow=''), follow=True, callback='parse'),
	)

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('h1.box-title-detail.entry-title') is None:
			return

		title = soup.select_one('h1.box-title-detail.entry-title').get_text(strip=True)
		time = soup.select_one('div.box-date').get_text(strip=True)
		summary = soup.select_one('div.box-des-detail p').get_text(strip=True)
		content_div = soup.select_one('div.detail-content-body')
		paragraphs = content_div.select('p')
		author = soup.select_one('div.box-author').get_text(strip=True)
		texts = [p.get_text(strip=True) for p in paragraphs if p is not None]
		content = '\n\n'.join([p for p in texts if p != ''])

		tags = []
		tags_ = soup.select_one('div.box-tags span').select('a')
		tags = [a.get_text(strip=True) for a in tags_]
		tags = [t for t in tags if t != '']

		extra_metadata = {'time': time, 'author': author, 'tags': tags}

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
