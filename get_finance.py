import requests
import json
from credentials import url, headers

ticker = "AAPL"

# Getting the data from https://docs.intrinio.com/documentation/api_v2/getting_started
with requests.Session() as session:
    session.headers.update(headers)

r = session.get(url + ticker, headers=headers)
json_data = json.loads(r.text)

# print(json.dumps(json_data, indent=2))
print("Website {} Name {}".format(json_data["company_url"], json_data["legal_name"]))
