import urllib2
# If you are using Python 3+, import urllib instead of urllib2

import json 

data =  {

        "Inputs": {

                "input1":
                {
                    "ColumnNames": ["idx", "age", "promotion_num", "identity", "game_play_min_per_day", "item_purchase_num_in_90_days", "game_level", "crystal", "race", "gender", "register_code", "purchase_num", "game_play_num_per_week", "country", "churn_YN"],
                    "Values": [ [ "0", "0", "0", "0", "0", "0", "0", "0", "value", "value", "0", "0", "0", "value", "value" ], [ "0", "30", "100", "300", "100", "00", "500", "300", "value", "value", "0", "0", "0", "value", "value" ], ]
                },        },
            "GlobalParameters": {
}
    }

body = str.encode(json.dumps(data))

url = 'https://asiasoutheast.services.azureml.net/workspaces/46d0e60b05b34558827abd41f11d204f/services/7e2a0a94ed4d40c1965b523707feea59/execute?api-version=2.0&details=true'
api_key = '<API_KEY>' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib2.Request(url, body, headers) 

try:
    response = urllib2.urlopen(req)

    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
    # req = urllib.request.Request(url, body, headers) 
    # response = urllib.request.urlopen(req)

    result = response.read()
    print(result) 
except urllib2.HTTPError, error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())

    print(json.loads(error.read()))       