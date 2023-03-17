from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http.request import Request
import json
import re
class CrawlingSpider(CrawlSpider):
    
    name = "mycrawler"
    allowed_domains = ["thanhnien.vn"]
    start_urls = ["https://thanhnien.vn/"]

    # PROXY_SERVER = "113.161.131.43"

    rules = (
        Rule(LinkExtractor(allow=r'[a-zA-Z]\.htm'), follow=True, callback=None),
        Rule(LinkExtractor(allow=r'[0-9]+\.htm'), follow=True, callback='parse_item'),
    )

    def parse_item(self, response):
        # C1:
        contents = response.css(".detail-content p::text").getall()           
        contents = "\n\n".join(contents)
        
        # C2:
        # contents = []
        # p_all = response.css(".detail-content p")
        # for p_sub in p_all:
        #     tag_p_s = p_sub.css("p::text").getall()
        #     tag_a_s = p_sub.css("a::text").getall()

        #     texts_1_line = tag_p_s + tag_a_s
        #     texts_1_line[::2] = tag_p_s
        #     texts_1_line[1::2] = tag_a_s
        #     texts_1_line = "".join(texts_1_line)

        #     contents.append(tag_p_s)

        # contents = "\n\n".join(texts_1_line)

        # C3: chua xong
        a = response.css(".detail-content")
        contents = [' '.join(line.strip() for line in p.xpath('.//text()').extract() if line.strip()) for p in a.css('p')]
        contents = "\n\n".join(contents)
        contents = re.sub(r"(\n)+", r"\n\n", contents)

        ''' giải thích dòng 32
        for p in a.css('p'):
            # Tách dòng văn bản thành danh sách các dòng b
            p.xpath('.//text()').extract() = p.split("\n")
            
            # Khởi tạo một chuỗi tạm thời cho phần tử của danh sách kết quả
            tmp = ""
            
            # Duyệt qua từng dòng trong danh sách b
            for line in p.xpath('.//text()').extract():
                # Xóa khoảng trắng ở đầu và cuối dòng, kiểm tra xem dòng có rỗng không
                line = line.strip()
                if line:
                    # Nếu dòng không rỗng, thêm nội dung của dòng vào chuỗi tạm thời
                    tmp += line + " "
            
            # Nếu chuỗi tạm thời không rỗng, thêm chuỗi vào danh sách kết quả
            if tmp:
                contents.append(tmp.strip())
        '''
                
        yield {
            "title": response.css(".detail-title span::text").get(),
            "url": response.css(".fb-like::attr(data-href)").extract()[0],
            "summary": response.css(".detail-sapo::text").get().strip(),
            "content": contents,
            "extra_metadata": {
                "date": response.css(".detail-time div::text").get().strip()
            }            
        }

        


    

