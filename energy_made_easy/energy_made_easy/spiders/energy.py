import scrapy
from scrapy_splash import SplashRequest

class EnergySpider(scrapy.Spider):
    name = 'energy'
    allowed_domains = ['www.energymadeeasy.gov.au']
    start_urls = ['http://www.energymadeeasy.gov.au/']

    def start_requests(self):
        yield SplashRequest(url=self.start_urls[0], callback=self.parse, endpoint="render.html", args={"wait": 0.5})
    
    def parse(self, response):
        for tar in response.xpath("//button[@id='get-started']"):
            yield 
