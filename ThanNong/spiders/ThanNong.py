from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class ThanNong(CrawlSpider):
	name = 'than-nong'
	start_urls = [
		'https://thannong.net/']
	allowed_domains = ['thannong.net']
	rules = [
		Rule(LinkExtractor(allow=''), follow=True, callback='parse')
	]

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('div.blog-meta-content h2') is None:
			return

		title = soup.select_one('div.blog-meta-content h2').get_text(strip=True)
		author = soup.select_one('dd.createdby').get_text(strip=True)
		time = soup.select_one('dd.published').get_text(strip=True)
		summary = ''
		content_div = soup.select_one('div.blog-content-wrap div')
		paragraphs = content_div.select('p')
		content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p is not None])

		tags = []
		tags_li = soup.select('ul.tag-b li.tag-item')[1:]
		tags = [li.get_text(strip=True) for li in tags_li if li is not None]
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
