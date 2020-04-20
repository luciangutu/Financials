import requests
import json
from pprint import pprint
from credentials import url, headers
from collections import OrderedDict
from operator import getitem

ticker = "AAPL"


# getting the statement_code IDs into a list
# {u'fun_X60lv6': {'fiscal_period': u'Q2', 'fiscal_year': 2018},
#  u'fun_X7BZMO': {'fiscal_period': u'Q4', 'fiscal_year': 2018}}
def get_statement_code_ids(statement_code_value):
    results = {}
    if "fundamentals" not in json_data:
        # if fundamentals key is not part of the JSON
        # check https://api-v2.intrinio.com/fundamentals/ID/reported_financials
        print("Cannot get statement for ID", statement_code_value)
        pprint(json_data)
        return None
    for sub in json_data["fundamentals"]:
        key, value = 'statement_code', statement_code_value
        if key in sub and value == sub[key]:
            # don't get the YTD, QxYTD or QxTTM
            if len(sub["fiscal_period"]) == 2:
                results[sub["id"]] = {}
                results[sub["id"]]["fiscal_year"] = sub["fiscal_year"]
                results[sub["id"]]["fiscal_period"] = sub["fiscal_period"]
    # have the dictionary sorted
    product_list = OrderedDict(sorted(results.items(), key=lambda k: getitem(k[1], 'fiscal_year')))
    return product_list

# print("Income statement")
# print(get_statement_code_ids('income_statement'))
# print("Balance Sheet statement")
# pprint(get_statement_code_ids('balance_sheet_statement'))
# print("CashFlow statement")
# pprint(get_statement_code_ids('cash_flow_statement'))


# Getting the data from https://docs.intrinio.com/documentation/api_v2/getting_started
with requests.Session() as session:
    session.headers.update(headers)

# getting the fundamental IDs
# https://api-v2.intrinio.com/companies/AAPL/fundamentals
r = session.get(url + "companies/" + ticker + "/fundamentals", headers=headers)
json_data = json.loads(r.text)

# getting reported financials for every income_statement
# https://api-v2.intrinio.com/fundamentals/ID/reported_financials
full_income_statement = get_statement_code_ids('income_statement')
for income in full_income_statement:
    print("Fiscal Year/Period {}/{}".format(full_income_statement[income]['fiscal_year'],
                                            full_income_statement[income]['fiscal_period']))
    r = session.get(url + "fundamentals/" + income + "/standardized_financials", headers=headers)
    try:
        json_data = json.loads(r.text)
    except ValueError as e:
        print("No data")
        continue

    if "standardized_financials" not in json_data or len(json_data['standardized_financials']) == 0:
        print("No data")
        continue

    print_only_tags = ['totalrevenue', 'totalcostofrevenue', 'totalgrossprofit', 'totaloperatingexpenses',
                       'totaloperatingincome', 'netincome', 'basiceps']

    for elem in json_data["standardized_financials"]:
        if elem["data_tag"]["tag"] in print_only_tags:
            print(elem["data_tag"]["name"]),
            # check if the value is positive or negative (balance)
            if elem["data_tag"]["balance"] == "debit":
                print("-{:,}".format(elem["value"]))
            else:
                print("{:,}".format(elem["value"]))
