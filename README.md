# Energy-Made-Easy-Scraper

Web site https://www.energymadeeasy.gov.au/ scraper to scrap energy plans against various options

This is a scrapy project to scrape different plans provided for fueltype (Electricity, Gas, Both) in yearly, quaterly, monthly bases according to specific needs.

In this project, I have integrated api of the website to get and post data:

User can give input to api request using `config.json` file provided in the scraper.

Config.json file has following inputs:

#### 1- "crawler_configuration": For using proxies, saving scraped data in specific format.

"use_proxy": (true or false)
"proxy": (null, or proxy),
"save_as_excel": (true or false),
"save_as_json": (true or false),
"save_to_google_sheets": (true or false)

#### 2- "scrap_all_energy_plans_internal_data": (true or false), # If want to scrap full details of the plans

#### 3- "energymadeeasy_inputs": # data to give for api request

"fuel_type": "E",
"post_code": "2000",
"state": "NSW",
"suburb": "Barangaroo",
"household_size": "L",
"customer_type": "R",
"bill_mode": "noUsageFrontier",
"isMeterDataRetrieved": false,
"meterDataInit": false,
"solarPanels": "",
"pool": "",
"underfloorHeating": "",
"gasMethod": "",
"gasHeater": "",
"smartMeter": "N",
"peakOffpeakRates": "",
"controlledLoad": "N",
"retailer-E": "notSure",
"retailer-G": "",
"distributor-E": "",
"distributor-G": "",
"gasBillStartDate": "",
"gasBillEndDate": "",
"electricityBillStartDate": "",
"electricityBillEndDate": "",
"terms_accepted": true,
"factors": [
{
"factorName": "ac",
"answer": "N",
"fuelType": "E"
},
{
"factorName": "cl",
"answer": "N",
"fuelType": "E"
},
{
"factorName": "sp",
"answer": "N",
"fuelType": "E"
}
],
"concessionsFromBills": {},
"benchmarkUsageType": ""
