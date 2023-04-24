from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class BoCongAn(CrawlSpider):
	name = 'bo-cong-an'
	allowed_domains = ['bocongan.gov.vn']
	start_urls = ['https://bocongan.gov.vn/']
	rules = (
		Rule(LinkExtractor(allow=['/pbgdpl/gioi-thieu-van-ban/', '/pbgdpl/tin-tuc/'], deny='/pbgdpl/van-ban-du-thao/'),
		     follow=True, callback='parse'),
	)

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('div.detailnew h1') is None:
			return

		title = soup.select_one('div.detailnew h1').get_text(strip=True)
		time = soup.select_one('div.time').get_text(strip=True)
		summary = soup.select_one('div.desc').get_text(strip=True)
		content_div = soup.select_one('div.detail')
		paragraphs = content_div.select('p')
		texts = [p.get_text(strip=True) for p in paragraphs if p is not None]
		content = '\n\n'.join([p for p in texts if p != ''])
		author = soup.select_one('div.tacgia').get_text(strip=True)

		tags = []
		tags_ = soup.select('div.tags ul li')
		tags = [a.get_text(strip=True) for a in tags_ if a is not None]
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
