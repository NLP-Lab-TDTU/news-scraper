from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class BaoTNMT(CrawlSpider):
	name = 'bao-tnmt'
	allowed_domains = ['baotainguyenmoitruong.vn']
	start_urls = ['https://baotainguyenmoitruong.vn/']
	rules = (
		Rule(LinkExtractor(allow='', deny='/an-pham/'), follow=True, callback='parse'),
	)

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('h1.c-detail-head__title') is None:
			return

		title = soup.select_one('h1.c-detail-head__title').get_text(strip=True)
		content_div = soup.select_one('div.b-maincontent')
		summary = content_div.find_all()[0].get_text(strip=True)
		paras = content_div.find_all()[2:]
		content = '\n\n'.join([p.get_text(strip=True) for p in paras if p is not None])

		tags = []
		tags_ = soup.select('div.c-tags ul li')
		tags = [a.get_text(strip=True) for a in tags_ if a is not None]
		tags = [t for t in tags if t != '']

		extra_metadata = {'time': '', 'author': '', 'tags': tags}

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

