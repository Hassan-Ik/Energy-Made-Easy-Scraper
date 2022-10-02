def request_body(fuel_type="E", post_code="2000", 
                 state="NSW", suburb="Barangaroo", household_size="L", 
                 customer_type="R", bill_mode="noUsageFrontier", terms_accepted=True):
    """
    This function adds our search filters, or our form data in the api request.
    
    ------------------------------------------
    Parameters
    
    fuel_type (str): It means, which energy type price are we checking 
                        i-e Gas, electricity etc, first option in form filling in website
    post_code (str): Post code of the area, second input in the form.
    state (str): used with second input in the form, it means which state to select from in the post_code.
    suburb (str): Also with the second input form.
    household_size (str): the size of the household i-e how many peoples in the house 1, 2, 3-5.0
    bill_mode (str): type of bill mode, i-e noUsageFrontier 
    terms_accepted (str): If terms are accepted or not. default is true.
    Args:
        fuel_type (_type_): _description_
        post_code (_type_): _description_
        customer_type (_type_): _description_
    """
    try:
        body = {
            "priceParams": {
            "postcode": post_code,
            "state": state,
            "suburb": suburb,
            "fuelType": fuel_type,
            "householdSize": household_size,
            "customerType": customer_type,
            "isMeterDataRetrieved": False,
            "meterDataInit": False,
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
            "acceptTerms": terms_accepted,
            "factors": [
                {
                    "factorName": "ac",
                    "answer": "N",
                    "fuelType": fuel_type
                },
                {
                    "factorName": "cl",
                    "answer": "N",
                    "fuelType": fuel_type
                },
                {
                    "factorName": "sp",
                    "answer": "N",
                    "fuelType": fuel_type
                }
            ],
            "billMode": bill_mode,
            "concessionsFromBills": {}
           },
            "postcode": post_code,
            "fuelType": fuel_type,
            "customerType": customer_type,
            "smartMeter": False,
            "solarPanels": False,
            "benchmarkUsageType": "",
            "billMode": bill_mode
        }
        return body
    except Exception as e:
        return e