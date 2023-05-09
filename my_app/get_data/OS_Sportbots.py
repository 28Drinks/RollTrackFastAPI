import requests
from collections import defaultdict
import json



def recursive_lower_keys(d):
    # convert all keys and keys in sub dicts to lowercase
    if isinstance(d, dict):
        return {k.lower(): recursive_lower_keys(v) for k, v in d.items()}
    else:
        return d

all_bots = []
x = 9990

while x < 10000:
    print(x)
    url = "https://api.opensea.io/api/v1/assets?token_ids=" + str(x) + "&collection=sportsbots&order_direction=desc&limit=1&include_orders=false"
    headers = {
        "Accept": "application/json",
        "X-API-KEY": ""
    }
    response1 = requests.request("GET", url, headers=headers)
    response = response1.json()


    try:
        bot_data_dict = dict()
        bot_data_dict = {"stats": {}, "traits": {}}
        traits = response["assets"][0]["traits"]

        bot_data_dict["name"] = response["assets"][0]["name"]
        bot_data_dict["number"] = int(response["assets"][0]["token_id"])
        bot_data_dict["image_url"] = response["assets"][0]["image_url"]

        if not traits:
            bot_data_dict["revealed"] = False

        else:
            bot_data_dict["revealed"] = True
            for trait in traits:
                if trait["trait_type"] in ["Sportshares", "Freebet", "Comboboost"]:
                    bot_data_dict["stats"][trait["trait_type"]] = trait["value"]
                else:
                    bot_data_dict["traits"][trait["trait_type"]] = trait["value"]


    except:
        pass

    x += 1

    bot_data_dict = recursive_lower_keys(bot_data_dict)

    #bot_data_dict = {k.lower(): v for k, v in bot_data_dict.items()}

    all_bots.append(bot_data_dict)

print(all_bots)


for bot in all_bots:
    api_url = "http://0.0.0.0:8000/api/sportbots/"

    payload = bot

    response = requests.post(api_url, json=payload, headers={'Content-Type': 'application/json'})

    print(response.status_code)
    print(response.json())
