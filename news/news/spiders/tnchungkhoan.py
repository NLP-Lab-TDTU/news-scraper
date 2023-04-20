import requests
from bs4 import BeautifulSoup
import re
import scrapy
import requests
from urllib.parse import urljoin
import sys
import logging

def getPage(url):
    '''
    This method get a url link and return a BeautifulSoup object
    '''
    req = requests.get(url)
    req.encoding = 'utf-8'
    return BeautifulSoup(req.text, "html.parser")

class Newspaper:
    def __init__(self, url):
        '''
        Construct a BeautifulSoup object from getPage method with argument 
        is a url link
        '''
        filter_str = ''.join([chr(i) for i in range(1, 32)])
        self.bs = getPage(url)
        
    def get_title(self, tag, class_of_tag):
        '''
        This method have argument is a tag and class of this tag.
        It return a title of a newspaper by bs.find() method.
        Argument:
            - tag: the tag cover content of the title
            - class_of_tag: class of the tag which is argument
        '''
        title = self.bs.find(tag, {"class": class_of_tag})
        return title.text
    
    def get_summary(self, tag, class_of_tag, children=""):
        '''
        This method return a summary of a newspaper by bs.find() method.
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
        return summary
    
    def get_tags(self, tag, class_of_tag, children = "a"):
        '''
        This method return a list contain the tags of a newspaper by bs.find() method.
        Argument:
            - tag: the tag cover content of the title
            - class_of_tag: class of the tag which is argument
            - children: the inner tag on a super class which cover the text
        '''
        tags = self.bs.find(tag, {"class": class_of_tag}).find_all(children)
        return [i.text for i in tags]
    
    
    def clean_sentence(self, sentence):
        pattern = re.compile(r'\s+')                             
        sentence = re.sub(pattern, ' ', sentence)
        return sentence.strip()

    
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
            texts = self.bs.find(tag, {"id": class_of_tag}).find_all(children)
            text = "\n\n".join([self.clean_sentence(i.text) for i in texts])
            return re.sub(r"\n{3,}", "\n\n", text)
        texts = self.bs.find(tag, {"class": class_of_tag}).find_all(children)
        text = "\n\n".join([self.clean_sentence(i.text) for i in texts])
        return re.sub(r"\n{3,}", "\n\n", text)
    

class TNCKSpider(scrapy.Spider):
    
    name = "tncktest"
    filter_str = ''.join([chr(i) for i in range(1, 32)])

    def start_requests(self):
        file = open("log_tnck.txt",'w')
        file.write("Logging file")
        base_url = 'https://www.tinnhanhchungkhoan.vn/'
        yield scrapy.Request(url=base_url, callback = self.parse_nav_link)
        zone = 0
        page = 0
        while zone > -1:
          zone = 2  
          api = f'https://api.tinnhanhchungkhoan.vn/api/morenews-zone:{zone}_{page}.html?phrase='
          res = requests.get(api).json()
          if res['error_message'] != 'Success':
            file.write("Done visiting apis")
            zone = -1
            break
          ## test-limit
          file.write(f"Visit OK - zone {zone}, page {page}: {api}")
          zone = -1

          for content in res['data']['contents']:
            new_url = urljoin(base_url,content['url'])
            yield scrapy.Request(url=new_url, callback=self.parse_item)
            break
          load_more = res['data']['load_more']
          if not load_more:
            file.write(f'Done at page: {page}')
            zone = zone+1 if zone != 9 else 11
            page = 0
          else:
              page += 1

    def parse_nav_link(self, response):
        pattern = 'https://www.tinnhanhchungkhoan.vn/'
        ul_tag = response.css('ul.box-bottom')
        links = ul_tag.css('li a::attr("href")').getall()
        links = [link for link in links if re.match(pattern,link)]
        for link in links:
            yield response.follow(link, self.parse_head_lines)

    def parse_head_lines(self, response):
        main = response.css('div.main-column').css('a.cms-link::attr("href")')
        links = list(set(main.getall()))
        links = [link for link in links if link.endswith('html')]
        for link in links:
            yield response.follow(link, self.parse_item)
            break

    def parse_item(self, response):
        newspaper = {}
        news = Newspaper(response.url)
        try:
            newspaper['title'] = news.get_title(tag="h1", class_of_tag="article__header")
            newspaper['summary'] = news.get_summary('div', 'article__sapo')
            newspaper['content'] = news.get_content('div', class_of_tag='article__body')
            for key in newspaper.keys():
                newspaper[key] = newspaper[key].translate(\
                        str.maketrans('','',TNCKSpider.filter_str)).strip()
            newspaper['url'] = response.url
            newspaper['extra_metadata'] = news.get_tags('div', 'article__tag')
            newspaper['time'] = news.get_date('time','time')
            return newspaper
        except ValueError:
            return {}

        

