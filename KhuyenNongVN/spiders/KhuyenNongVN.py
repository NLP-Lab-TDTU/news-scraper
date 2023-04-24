from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re


class KhuyenNongVN(CrawlSpider):
	name = 'khuyen-nong-vn'
	start_urls = [
		'https://khuyennongvn.gov.vn/']
	allowed_domains = ['khuyennongvn.gov.vn']
	rules = [
		Rule(LinkExtractor(
			allow=['/hoat-dong-khuyen-nong/', '/chuong-trinh-nganh-nong-nghiep/', '/khoa-hoc-cong-nghe/']),
			follow=True, callback='parse')
	]

	def parse(self, response):
		soup = BeautifulSoup(response.body, 'html.parser')

		if soup.select_one('h1.post-title') is None:
			return

		title = soup.select_one('h1.post-title').get_text(strip=True)
		author = ''
		time = soup.select_one('div.lbPublishedDate').get_text(strip=True)
		summary = soup.select_one('div.postsummary').get_text(strip=True)
		content_div = soup.select_one('div.noidung')
		paragraphs = content_div.select('p')
		content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
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
