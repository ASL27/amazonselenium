from email.mime import base
import scrapy
# 引入settings
from scrapy.utils.project import get_project_settings
from urllib.parse import urlencode
from amazonselenium.items import AmazonseleniumItem
import time
# from scrapy import Request, Spider
settings = get_project_settings()

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.cn']
    start_urls = ['http://www.amazon.cn/']
    
    def start_requests(self):
        # https://www.amazon.cn/s?k=iPad&__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&crid=UH9JRIHEWIMZ&sprefix=ipad%2Caps%2C140&ref=nb_sb_noss_1
        base_url = 'https://www.amazon.cn/s?'
        # https://www.amazon.cn/s?k=ipad&page=2
        # data = {'k':'ipad', 'page': '1', 'crid': '31DTEW5X7KV5Q', 'qid': '1660806360', 'sprefix': 'ipad%2Caps%2C96', 'ref': 'sr_pg_1'}
        data = {'k':'ipad', 'page': '1'}
        for keyword in settings['KEYWORDS']:
            data['k'] = keyword
            # data['sprefix'] = 'ipad%2Caps%2C96'
            for page in range(1, settings['MAX_PAGE'] + 1):

                # data['qid'] = int(time.time())
                data['page'] = str(page)
                # data['ref'] = 'sr_pg_' + str(page)
                # 拼成链接
                params = urlencode(data)
                if page > 1:
                    amazon_url = base_url + params
                else:
                    amazon_url = 'https://www.amazon.cn/s?k=ipad'
                print(amazon_url)
                yield scrapy.Request(url=amazon_url, callback=self.parse,dont_filter=True)

    def parse(self, response):

        for data in response.xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div'):
            images = data.re(r'<img class="s-image" src="(.*?)" srcset="" alt=".*?" data-image-index=".*?" data-image-load=.*?data-image-latency=.*?>')
            title = data.re(r'<span class="a-size-base-plus a-color-base a-text-normal">(.*?)</span>')
            price = data.re(r'<span class="a-offscreen">(¥.*?.\d{2})</span>')
            star = data.re(r'<span class="a-icon-alt">(\d.\d) 颗星，最多 5 颗星</span>')
            # <span class="a-icon-alt">3.5 颗星，最多 5 颗星</span>
            # <span class="a-offscreen">¥266.78</span>
            # <span class="a-size-base-plus a-color-base a-text-normal">OtterBox Pad Mini 5 代 TRUSTY 外壳 - YOYO</span>          
            if images ==[] and title ==[] and price  ==[] and  star ==[]:
                continue
            item = AmazonseleniumItem()
            
            item['images'] = ''.join(images)
            item['title'] = ''.join(title)
            item['price'] = ''.join(price)
            item['star'] = ''.join(star)
            yield item
        # print(response.text)
        

