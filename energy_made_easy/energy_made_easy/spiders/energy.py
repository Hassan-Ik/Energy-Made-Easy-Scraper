import json
import scrapy
from scrapy_splash import SplashRequest
from http.client import responses
from .body_request_object import request_body
from user_agent import generate_user_agent

class EnergySpider(scrapy.Spider):
    name = 'energy'
    allowed_domains = ['www.energymadeeasy.gov.au']
    
    user_agent = generate_user_agent()
    headers =  {
            "authority": "api.energymadeeasy.gov.au",
            "method": "POST",
            "path": "/plans/dpids/prices",
            "scheme": "https",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json;charset=UTF-8",
            'origin': 'https://www.energymadeeasy.gov.au',
            'Referer': 'https://www.energymadeeasy.gov.au/',
            'User-Agent': user_agent
            # 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',
        }
    
    def start_requests(self):
        body = request_body()
        
        api_request_url = "https://api.energymadeeasy.gov.au/plans/dpids/prices"
        
        yield scrapy.Request(
            api_request_url, 
            method='POST',
            body=json.dumps(body),
            headers=self.headers,
            callback=self.parse)
        
    def parse(self, response):
        
        plans = json.loads(response.body)
        
        for plan in plans:
            yield self.request_price_plans(plan["planId"], plan["postcode"])
    
    def request_price_plans(self, plan_id, post_code):
        plan_request_url = "https://api.energymadeeasy.gov.au/plans/dpids/" + plan_id + post_code 
        yield scrapy.Request(plan_request_url, method="GET", headers=self.headers, callback=self.parse_price_plans)
    
    def parse_price_plans(self, response):
        pass