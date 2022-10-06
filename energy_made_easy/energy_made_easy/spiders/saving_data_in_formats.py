import json
import pandas as pd
import os

def save_data_to_csv(json_response, fuel_type, post_code, state , household_size ,customer_type):
    try:
        current_path = os.getcwd()
        file_path = current_path + fuel_type + post_code + state + household_size + customer_type + ".csv"
        
        if not os.exists(file_path):
            pd.DataFrame(
                {}
            )        
        
    except Exception as e:
        return e

def save_data_to_json(json_response, fuel_type, post_code, state , household_size ,customer_type):
    try:
        current_path = os.getcwd()
        current_path = current_path.replace("\\", "/")
        current_path = os.path.join(current_path, "energy_made_easy")
        current_path = current_path.replace("\\", "/") 
        
        file_path = current_path + "/" + fuel_type + post_code + state + household_size + customer_type + ".json"
        
        with open(file_path, 'wb') as filehandler:
            json.dump(json_response, filehandler)
    
    except Exception as e:
        return e

def save_plan_data_to_json(json_response):
    try:
        current_path = os.getcwd()
        current_path = os.getcwd()
        current_path = current_path.replace("\\", "/")
        current_path = os.path.join(current_path, "energy_made_easy")
        current_path = current_path.replace("\\", "/")
        
        file_path = current_path + "/" + "plan_data" + ".json"
        
        with open(file_path, 'wb') as filehandler:
            json.dump(json_response, filehandler)
    
    except Exception as e:
        return e