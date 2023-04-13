from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from forbesvn.items import ForbesvnItem
import requests
from bs4 import BeautifulSoup
import re

class Newspaper:


    def __init__(self, url):
        '''
        Construct a BeautifulSoup object from getPage method with argument 
        is a url link
        '''
        self.url = url
        self.bs = self.get_page()
        
    def get_page(self):
        req = requests.get(self.url)
        return BeautifulSoup(req.text, 'html.parser')
    
    def get_title(self, tag, class_of_tag):
        '''
        This method have argument is a tag and class of this tag.
        It return a title of a newspaper by bs.find() method.
        Argument:
            - tag: the tag cover content of the title
            - class_of_tag: class of the tag which is argument
        '''
        title = self.bs.find(tag, {"class": class_of_tag})
        return title.text.strip() if title else None
    
    def get_summary(self, tag, class_of_tag):
        '''
        This method return a summary of a newspaper by bs.find() method.
        Argument:
            - tag: the tag cover content of the title
            - class_of_tag: class of the tag which is argument
            - children: the inner tag on a super class which cover the text
        '''
        summary = self.bs.find(str(tag), {"class": class_of_tag})
        
        return summary.text.strip() if summary else None
    
    def get_date(self, tag, class_of_tag, children=""):
        '''
        This method return a publich day of a newspaper by bs.find() method.
        Argument:
            - tag: the tag cover content of the title
            - class_of_tag: class of the tag which is argument
            - children: the inner tag on a super class which cover the text
        '''
        if children != "":
            summary = self.bs.find(tag, {"class": class_of_tag}).find(children).text
            return summary
        summary = self.bs.find(tag, {"class": class_of_tag}).text
        return summary.strip()
    
    def get_tags(self, tag, class_of_tag, children = "a"):
        '''
        This method return a list contain the tags of a newspaper by bs.find() method.
        Argument:
            - tag: the tag cover content of the title
            - class_of_tag: class of the tag which is argument
            - children: the inner tag on a super class which cover the text
        '''
        tags = self.bs.find(tag, {"class": class_of_tag})
        
        if tags:
            tags_out = tags.find_all(children)
            return [i.text for i in tags_out]
        return None
    
    def clean_sentence(self, sentence):
        pattern = re.compile(r'\s+')                             
        sentence = re.sub(pattern, ' ', sentence)
        return sentence

    
    def get_content(self, tag, class_of_tag, children="p", _class=True):
        '''
        This method return texts of a newspaper by bs.find() method.
        After that, it join the texts together by "\n\n".join() method.
        Finally, replace \n >= 3 by \n\n
        Argument:
            - tag: the tag cover content of the title
            - class_of_tag: class of the tag which is argument
            - children: the inner tag on a super class which cover the text
        '''
        if _class == False:
            texts = self.bs.find(tag, {"class": class_of_tag}).find_all(children)
            text = "\n\n".join([self.clean_sentence(i.text) for i in texts])
            return re.sub(r"\n{3,}", "\n\n", text)
        texts = self.bs.find(tag, {"class": class_of_tag}).find_all(children)
        text = "\n\n".join([self.clean_sentence(i.text) for i in texts])
        return re.sub(r"\n{3,}", "\n\n", text)


class ArticleSpider(CrawlSpider):
    filter_str = ''.join([chr(i) for i in range(1, 32)])
    name = 'forbesvn'
    allowed_domains = ['forbes.vn']
    start_urls = ['https://forbes.vn/tesla-ghi-nhan-so-luong-xe-ban-giao-cho-khach-trong-quy-1-tang-36']
    
    rules = [
        Rule(LinkExtractor(allow=r'^https:\/\/forbes\.vn\/.*'), callback='parse_item', follow=True),
    ]
    
    def f1(self, texts):
        return ''.join([i.strip() for i in texts])

    def parse_item(self, response):
        try:
            newspaper = ForbesvnItem()
            url = response.url
            news = Newspaper(url)
            newspaper['title'] = news.get_title(tag="h1", class_of_tag="forbes-single__heading-title")
            if newspaper['title'] is None:
              return
            newspaper['url'] = url
            newspaper['summary'] = news.get_summary('div', 'forbes-short-description__container')
            newspaper['content'] = news.get_content('div', class_of_tag='forbes-container mt-32 forbes-mb-80 forbes-position-relative px-0')
            newspaper['extra_metadata'] = news.get_tags('div','forbes-single__tags')
            newspaper['content'] = self.clean(newspaper['content'])
            return newspaper
        except Exception as e:
            print(e)
    
    def clean(self,sentence):
        tmp = sentence.translate(str.maketrans('','',ArticleSpider.filter_str))
        sentence = tmp.replace(" +"," ").strip()
        return sentence
    
    
