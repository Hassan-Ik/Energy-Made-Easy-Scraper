import json
import scrapy
from scrapy_splash import SplashRequest
from http.client import responses
from .body_request_object import body_for_api_request
from scrapy.crawler import CrawlerProcess
from user_agent import generate_user_agent
from .proxy import ProxySpider

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
        
        with open("../config.json") as config_f:
            config = json.loads(config_f)
        
        self.use_proxy = config["crawler_configuration"]["use_proxy"]
        self.save_as_excel = config["crawler_configuration"]["save_as_excel"]
        self.save_as_json = config["crawler_configuration"]["save_as_json"]
        self.scrap_all_energy_plans_internal_data = config["scrap_all_energy_plans_internal_data"]
        
        if self.use_proxy:
            process = CrawlerProcess()
            process.crawl(ProxySpider)
            process.start()
        
        fuel_type = config["energymadeeasy_inputs"]["fuel_type"]
        post_code = config["energymadeeasy_inputs"]["post_code"]
        state = config["energymadeeasy_inputs"]["state"]
        suburb = config["energymadeeasy_inputs"]["suburb"]
        household_size = config["energymadeeasy_inputs"]["household_size"]
        customer_type = config["energymadeeasy_inputs"]["customer_type"]
        bill_mode = config["energymadeeasy_inputs"]["bill_mode"]
        isMeterDataRetrived = config["energymadeeasy_inputs"]["isMeterDataRetrieved"]
        meterDateInit = config["energymadeeasy_inputs"]["meterDataInit"]
        solarPanels = config["energymadeeasy_inputs"]["solarPanels"]
        pool = config["energymadeeasy_inputs"]["pool"]
        underfloorHeating = config["energymadeeasy_inputs"]["underfloorHeating"]
        gasMethod = config["energymadeeasy_inputs"]["gasMethod"]
        gasHeater = config["energymadeeasy_inputs"]["gasHeater"]
        smartMeter = config["energymadeeasy_inputs"]["smartMeter"]
        peakOffpeakRates = config["energymadeeasy_inputs"]["peakOffpeakRates"]
        controlledLoad = config["energymadeeasy_inputs"]["controlledLoad"]
        retailer_E = config["energymadeeasy_inputs"]["retailer-E"]
        retailer_G = config["energymadeeasy_inputs"]["retailer-G"]
        distributor_E = config["energymadeeasy_inputs"]["distributor-E"]
        distributor_G = config["energymadeeasy_inputs"]["distributor-G"]
        gasBillStartDate = config["energymadeeasy_inputs"]["gasBillStartDate"]
        gasBillEndDate = config["energymadeeasy_inputs"]["gasBillEndDate"]
        electricityBillStartDate = config["energymadeeasy_inputs"]["electricityBillStartDate"]
        electricityBillEndDate = config["energymadeeasy_inputs"]["electricityBillEndDate"]
        terms_accepted = config["energymadeeasy_inputs"]["terms_accepted"]
        factors = config["energymadeeasy_inputs"]["factors"]
        concessionsFromBills = config["energymadeeasy_inputs"]["concessionsFromBills"]
        benchmarkUsageType = config["energymadeeasy_inputs"]["benchmarkUsageType"]
        
        
        if terms_accepted == False:
            return "Terms and conditions should be accepted else, request will not be processed"
        
        body = body_for_api_request()
        
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
        response = json.loads(response.body)
        yield response