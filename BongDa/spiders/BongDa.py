from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class Bongda(CrawlSpider):
	name = 'bong-da'
	allowed_domains = ['bongda.com.vn']
	start_urls = ['https://www.bongda.com.vn/']
	rules = (
		Rule(LinkExtractor(allow=''), follow=True, callback='parse'),
	)

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('h1.time_detail_news') is None:
			return

		title = soup.select_one('h1.time_detail_news').get_text(strip=True)
		summary = soup.select_one('p.sapo_detail').get_text(strip=True)
		time = soup.select_one('div.time_comment').get_text(strip=True)
		content_div = soup.select_one('div.news_details')
		paras = content_div.select('p')
		content = '\n\n'.join([p.get_text(strip=True) for p in paras])
		tags_div = soup.select_one('div.list_tag_trend').select('a')
		tags = []
		tags = [a.get_text(strip=True) for a in tags_div if a is not None]
		extra_metadata = dict()
		extra_metadata['time'] = time
		extra_metadata['author'] = ''
		extra_metadata['tags'] = tags

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
