import time
import scrapy
from user_agent import generate_user_agent
from .utils import get_port_number
import json

class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['www.spys.one']
    
    
    user_agent = generate_user_agent()
    proxy_countries = [
        "AU",
        "US",
        "NL",
        "GB",
        "SG",
        "DE",
        "FR",
        "IN"
    ]
        
    headers =  {
            'origin': 'https://spys.one/',
            'Referer': 'https://spys.one/',
            'User-Agent': user_agent
            # 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36'
        }
    
    def start_requests(self):
        for country in self.proxy_countries:
            time.sleep(1)      
            yield scrapy.Request(url = f"https://spys.one/free-proxy-list/{country}/", method="GET", headers=self.headers, callback=self.parse)

    def parse(self, response):
        iter = 0
        # split = response.body.decode('utf-8')
        # split = split.strip()
        proxies = response.xpath("//table")
        proxies_table = proxies[2].xpath("//tr[@class='spy1xx' or @class='spy1x']")
        for proxy in proxies_table:
            
            if iter < 2:
                iter += 1
                continue
            
            proxy_type_fonts = proxy.css("td:nth-child(2) > a > font::text").extract()
            
            proxy_type = ""
            for p in proxy_type_fonts:
                proxy_type += p
            
            if proxy_type == "HTTPS":
                port = proxy.css("script::text").extract_first()
                port = get_port_number(port)
                proxy = proxy.css("td:nth-child(1) > font::text").extract()[0]
                print(port)
                print(proxy)
                yield proxy
        