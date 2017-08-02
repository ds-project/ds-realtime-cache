import os
import json
import urllib.request
import redis

# set configs
redis_host = '<redis host>'
auth_key = '<redis auth key>'
redis_db = redis.StrictRedis(host=redis_host, port=6379, db=0, password=auth_key)

url = '<azure ml endpoint>'
api_key = '<azure ml api key>'
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
redis_expire = 3600

postreqdata = json.loads(open(os.environ['req']).read())
inputs = postreqdata['inputs']

# make template of data to accept on azure ML
data_template =  {
        "Inputs": {
                "input1":
                {
                    "ColumnNames": ["idx", "age", "promotion_num", "identity", "game_play_min_per_day", "item_purchase_num_in_90_days", "game_level", "crystal", "race", "gender", "register_code", "purchase_num", "game_play_num_per_week", "country", "churn_YN"],
                    "Values": [  ]
                },        
            },
        "GlobalParameters": {}
    }

# function for sending data to ML
def do_ml_request(data):
    body = str.encode(json.dumps(data_template))
    req = urllib.request.Request(url, body, headers) 

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return result 
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.reason)


result_set = dict()
target_instance_list = list()

# filter user index list we should do request
for instance in inputs:
    user_idx = instance[0]
    print('Trying to hit redis User #' + user_idx)
    result_cached = redis_db.get(user_idx)

    if result_cached is None:
        target_instance_list.append(instance)
    else:
        print('Using Cached Data!')
        result_set[user_idx] = result_cached.decode("utf-8")

# If we should do request,
if len(target_instance_list) > 0:
    data_template["Inputs"]["input1"]["Values"] = target_instance_list
    result = do_ml_request(data_template).decode("utf-8") 
    result = json.loads(result)['Results']['output1']['value']['Values']
    for key, val in enumerate(result):
        user_idx = target_instance_list[key][0]
        result_set[user_idx] = val
        redis_db.set(user_idx, val, ex=redis_expire)

# fill response
print(result_set)
response = open(os.environ['res'], 'w')
response.write(json.dumps(result_set))
response.close()
