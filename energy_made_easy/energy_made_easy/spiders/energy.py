import os
import json
import scrapy
from .saving_data_in_formats import save_data_to_json, save_plan_data_to_json
from .body_request_object import body_for_api_request
from user_agent import generate_user_agent
import time
import random


class EnergySpider(scrapy.Spider):
    name = 'energy'
    allowed_domains = ['www.energymadeeasy.gov.au']
    
    def __init__(self):
        
        current_path = os.getcwd()
        current_path = current_path.replace("\\", "/")
        current_path = os.path.join(current_path, "energy_made_easy")
        config_file = os.path.join(current_path, "config.json")
        config_file = config_file.replace("\\", "/") 
        
        self.user_agent = generate_user_agent()
        
        self.headers =  {
                "authority": "api.energymadeeasy.gov.au",
                "path": "/plans/dpids/prices",
                "scheme": "https",
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "content-type": "application/json;charset=UTF-8",
                'origin': 'https://www.energymadeeasy.gov.au',
                'Referer': 'https://www.energymadeeasy.gov.au/',
                'User-Agent': self.user_agent
                #Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36
                # 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',
            }
        
        with open(config_file) as config_f:
            config = json.load(config_f)
            
        self.use_proxy = config["crawler_configuration"]["use_proxy"]
        self.save_as_excel = config["crawler_configuration"]["save_as_excel"]
        self.save_as_json = config["crawler_configuration"]["save_as_json"]
        self.scrap_all_energy_plans_internal_data = config["scrap_all_energy_plans_internal_data"]
        if self.use_proxy:    
            self.proxy = config["crawler_configuration"]["proxy"]
        
        self.fuel_type = config["energymadeeasy_inputs"]["fuel_type"]
        self.post_code = config["energymadeeasy_inputs"]["post_code"]
        self.state = config["energymadeeasy_inputs"]["state"]
        self.suburb = config["energymadeeasy_inputs"]["suburb"]
        self.household_size = config["energymadeeasy_inputs"]["household_size"]
        self.customer_type = config["energymadeeasy_inputs"]["customer_type"]
        self.bill_mode = config["energymadeeasy_inputs"]["bill_mode"]
        self.isMeterDataRetrieved = config["energymadeeasy_inputs"]["isMeterDataRetrieved"]
        self.meterDataInit = config["energymadeeasy_inputs"]["meterDataInit"]
        self.solarPanels = config["energymadeeasy_inputs"]["solarPanels"]
        self.pool = config["energymadeeasy_inputs"]["pool"]
        self.underfloorHeating = config["energymadeeasy_inputs"]["underfloorHeating"]
        self.gasMethod = config["energymadeeasy_inputs"]["gasMethod"]
        self.gasHeater = config["energymadeeasy_inputs"]["gasHeater"]
        self.smartMeter = config["energymadeeasy_inputs"]["smartMeter"]
        self.peakOffpeakRates = config["energymadeeasy_inputs"]["peakOffpeakRates"]
        self.controlledLoad = config["energymadeeasy_inputs"]["controlledLoad"]
        self.retailer_E = config["energymadeeasy_inputs"]["retailer-E"]
        self.retailer_G = config["energymadeeasy_inputs"]["retailer-G"]
        self.distributor_E = config["energymadeeasy_inputs"]["distributor-E"]
        self.distributor_G = config["energymadeeasy_inputs"]["distributor-G"]
        self.gasBillStartDate = config["energymadeeasy_inputs"]["gasBillStartDate"]
        self.gasBillEndDate = config["energymadeeasy_inputs"]["gasBillEndDate"]
        self.electricityBillStartDate = config["energymadeeasy_inputs"]["electricityBillStartDate"]
        self.electricityBillEndDate = config["energymadeeasy_inputs"]["electricityBillEndDate"]
        self.terms_accepted = config["energymadeeasy_inputs"]["terms_accepted"]
        self.factors = config["energymadeeasy_inputs"]["factors"]
        self.concessionsFromBills = config["energymadeeasy_inputs"]["concessionsFromBills"]
        self.benchmarkUsageType = config["energymadeeasy_inputs"]["benchmarkUsageType"]
    
    def start_requests(self):
        
        if self.terms_accepted == False:
            return "Terms and conditions should be accepted else, request will not be processed"
        
        body = body_for_api_request(self.fuel_type, self.post_code, 
                 self.state, self.suburb, self.household_size, 
                 self.customer_type, self.bill_mode, self.isMeterDataRetrieved, self.meterDataInit,
                 self.solarPanels, self.pool, self.underfloorHeating,
                 self.gasMethod, self.gasHeater, self.smartMeter, self.peakOffpeakRates,
                 self.controlledLoad,self.retailer_E,self.retailer_G,self.distributor_E,
                 self.distributor_G, self.gasBillStartDate, self.gasBillEndDate,
                 self.electricityBillStartDate,self.electricityBillEndDate,
                 self.factors,self.concessionsFromBills,self.benchmarkUsageType, self.terms_accepted)
        
        api_request_url = "https://api.energymadeeasy.gov.au/plans/dpids/prices"
        
        yield scrapy.Request(
            api_request_url, 
            method='POST',
            body=json.dumps(body),
            headers=self.headers,
            callback=self.parse)
        
    def parse(self, response):
        json_response = json.loads(response.body)
        
        if self.save_as_json: 
            save_data_to_json(json_response, self.fuel_type, self.post_code, self.state , self.household_size ,self.customer_type)
            
        if self.save_as_excel:
            pass
        random_sleep = [3,4,5,6,7]
        if self.scrap_all_energy_plans_internal_data:        
            for plan in json_response:
                time.sleep(random.choice(random_sleep))
                plan_request_url = "https://api.energymadeeasy.gov.au/plans/dpids/" + plan["planId"] + "?postcode=" + plan["post_code"]
                yield scrapy.Request(plan_request_url, method="GET", headers=self.headers, callback=self.parse_price_plans)
        
    def parse_price_plans(self, response):
        response = json.loads(response.body)
        if self.save_as_json:
            save_plan_data_to_json(response)
        
        if self.save_as_excel:
            pass
        
        yield