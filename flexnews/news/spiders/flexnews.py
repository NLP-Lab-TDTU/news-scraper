"""
Author: Nguyen Trong Hieu
"""

import hashlib
import re

import scrapy
from newspaper import Article, Source
from newspaper.configuration import Configuration
from newspaper.extractors import ContentExtractor
from scrapy.spiders import CrawlSpider

from ..items import NewsItem


class FlexSpider(CrawlSpider):
    name = "flexnews"
    allowed_domains = []
    start_urls = []

    news3k_config = Configuration()
    news3k_extractor = ContentExtractor(news3k_config)

    def __init__(self, domain, url):
        self.allowed_domains = [domain]
        self.start_urls = [url]

    @property
    def header(self):
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_categories)

    def parse_categories(self, response):
        source = Source(url=response.url, config=None)
        source.html = response.text
        source.parse()

        source.set_categories()
        source.download_categories()
        source.parse_categories()

        for category in source.category_urls():
            yield scrapy.Request(url=category, callback=self.parse, headers=self.header)

        if len(source.categories) == 1:
            url_title_tups = self.news3k_extractor.get_urls(source.doc, titles=True)
            for tup in url_title_tups:
                indiv_url = tup[0]
                indiv_title = tup[1]
                sub_item = Article(
                    url=indiv_url,
                    source_url=source.url,
                    title=indiv_title,
                    config=self.news3k_config
                )
                sub_item_url = sub_item.url
                sub_item_url = re.sub('#.*$', '', sub_item_url)
                if sub_item_url.startswith('http://') or sub_item_url.startswith('https://'):
                    yield scrapy.Request(url=sub_item_url, callback=self.parse, headers=self.header)

    def parse(self, response):
        item = Article(response.url, keep_article_html=True)
        item.set_html(response.body)
        item.parse()

        if item.is_media_news():
            return
        if item.meta_lang != 'vi':
            return

        category = item
        url_title_tups = self.news3k_extractor.get_urls(item.doc, titles=True)

        for tup in url_title_tups:
            indiv_url = tup[0]
            indiv_title = tup[1]
            sub_item = Article(
                url=indiv_url,
                source_url=category.url,
                title=indiv_title,
                config=self.news3k_config
            )
            sub_item_url = sub_item.url
            sub_item_url = re.sub('#.*$', '', sub_item_url)
            if sub_item_url.startswith('http://') or sub_item_url.startswith('https://'):
                yield scrapy.Request(url=sub_item_url, callback=self.parse, headers=self.header)

        if not item.is_valid_body():
            return
        else:
            article = item
            if article.is_media_news():
                return
            if article.meta_lang != 'vi':
                return

            title = article.title
            summary = ""
            content = article.text

            extra_metadata = {
                'id': hashlib.md5(article.url.encode('utf-8')).hexdigest(),
                'date': str(article.publish_date),
            }

            yield NewsItem(
                title=title,
                summary=summary,
                content=content,
                url=response.url,
                extra_metadata=extra_metadata
            )
