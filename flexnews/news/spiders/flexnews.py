"""
Author: Nguyen Trong Hieu
"""

import json
import re
import unicodedata

import markdownify
import scrapy
from newspaper.extractors import ContentExtractor
from newspaper.configuration import Configuration
from newspaper import Article
from newspaper import Source
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import NewsItem

class FlexSpider(CrawlSpider):
    name = "flexnews"
    allowed_domains = []
    start_urls = [
        "https://vnexpress.net/",
        "https://dantri.com.vn/",
        "https://tuoitre.vn/",
        "https://thanhnien.vn/",
        "https://vietnamnet.vn/",
        "https://zingnews.vn/",
        "https://baomoi.com/",
        "https://vtv.vn/",
        "https://laodong.vn/",
        "https://ngoisao.net/",
        "https://vietnammoi.vn/",
        "https://vietnamplus.vn/",
        "https://vov.vn/",
        "https://tienphong.vn/",
        "https://soha.vn/",
        "https://plo.vn/",
        "https://baotintuc.vn/",
        "https://baodautu.vn/",
        "https://haiquanonline.com.vn/",
    ]

    rules = [
        Rule(LinkExtractor(allow=r'https:.*')),
    ]

    news3k_config = Configuration()
    news3k_extractor = ContentExtractor(news3k_config)

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
                'id': article.link_hash,
                'date': str(article.publish_date),
            }

            yield NewsItem(
                title=title,
                summary=summary,
                content=content,
                url=response.url,
                extra_metadata=extra_metadata
            )
