from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class BongDa24h(CrawlSpider):
	name = 'bong-da-24h'
	start_urls = ['https://bongda24h.vn/']
	allowed_domains = ['bongda24h.vn']
	rules = [
		Rule(LinkExtractor(allow='', deny='/video/'), follow=True, callback='parse')
	]

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('h1.the-article-title') is None:
			return

		title = soup.select_one('h1.the-article-title').get_text(strip=True)
		time = soup.select_one('p.the-article-time').get_text(strip=True)
		author = soup.select_one('a.name-author').get_text(strip=True)
		content_div = soup.select_one('div.the-article-content')
		summary = content_div.select_one('div.summary').get_text(strip=True)
		tags = content_div.find_all(recursive=False)
		detail_list = []
		for tag in tags:
			if tag.name == 'div' and 'summary' in tag.get('class', []):
				continue
			else:
				detail_list.append(tag.get_text(strip=True))
		content = '\n\n'.join([p.strip() for p in detail_list if p])
		tags = []
		tags_div = soup.select('div.the-article-tags a')
		tags = [a.get_text(strip=True) for a in tags_div if a is not None]
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
