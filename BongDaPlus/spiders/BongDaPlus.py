from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class BongDaPlus(CrawlSpider):
	name = 'bong-da-plus'
	start_urls = [
		'https://bongdaplus.vn/']
	allowed_domains = ['bongdaplus.vn']
	rules = [
		Rule(LinkExtractor(
			allow=['/euro-cup-chau-au/', '/doi-tuyen-quoc-gia-viet-nam/', '/sea-games/', '/world-cup/', '/soi-keo/',
			       '/champions-league-cup-c1/', '/europa-league/', '/bong-da-tay-ban-nha/']),
			follow=True, callback='parse')
	]

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('h1.artitle') is None:
			return

		title = soup.select_one('h1.artitle').get_text(strip=True)
		author = soup.select_one('a.writer').get_text(strip=True)
		time = soup.select_one('div.dtepub').get_text(strip=True)
		summary = soup.select_one('div.summary').get_text(strip=True)
		content_div = soup.select_one('div#postContent')
		paragraphs = content_div.select('p')
		tags = []
		tags_ = soup.select('a.hashtag')
		tags = [a.get_text(strip=True) for a in tags_ if a is not None]
		content = '\n\n'.join([p.get_text(strip=False) for p in paragraphs])
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