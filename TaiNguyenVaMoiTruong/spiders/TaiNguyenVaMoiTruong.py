from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class TaiNguyenVaMoiTruong(CrawlSpider):
	name = 'tai-nguyen-va-moi-truong'
	allowed_domains = ['tainguyenvamoitruong.vn']
	start_urls = ['https://tainguyenvamoitruong.vn/']
	rules = (
		Rule(LinkExtractor(allow=''), follow=True, callback='parse'),
	)

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('h2.headingDetail') is None:
			return

		title = soup.select_one('h2.headingDetail').get_text(strip=False)
		time = soup.select_one('span.time').get_text(strip=True)
		summary = soup.select_one('p.descDetail').get_text(strip=True)
		content_div = soup.select_one('div.html-content')
		paragraphs = content_div.select('p')
		texts = [p.get_text(strip=True) for p in paragraphs if p is not None]
		content = '\n\n'.join([p for p in texts if p != ''])
		extra_metadata = {'time': time, 'author': ''}

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

