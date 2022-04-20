import requests
import json
class Api:
    def __init__(self):
        pass

    def makeApiRequestForCounrty(self, country_name):
        querystring = {"country": country_name}
        url = "https://covid-193.p.rapidapi.com/statistics"

        headers = {
        "X-RapidAPI-Host": "covid-193.p.rapidapi.com",
        "X-RapidAPI-Key": "b345b2cdc4msh07c26d5b719c459p1bbfe7jsn5764aff56625"
                 }
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.text)
        js = json.loads(response.text)
        print("******", js)
        result = js.get('response')[0]
        print(result.get('cases'))
        print("*" * 20)
        return result.get('cases') , result.get('deaths'),result.get('tests')


    def makeApiRequestForIndianStates(self):
        url = "https://covid-193.p.rapidapi.com/countries"
        querystring = {"search":"india"}
        headers = {
        "X-RapidAPI-Host": "covid-193.p.rapidapi.com",
        "X-RapidAPI-Key": "b345b2cdc4msh07c26d5b719c459p1bbfe7jsn5764aff56625"
                 }
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.text)
        js = json.loads(response.text)
        print("******", js)
        #result = js.get('list')
        return js


    def makeApiWorldwide(self):
        url= "https://covid-19-statistics.p.rapidapi.com/reports/total"
        headers = {
        "X-RapidAPI-Host": "covid-19-statistics.p.rapidapi.com",
        "X-RapidAPI-Key": "b345b2cdc4msh07c26d5b719c459p1bbfe7jsn5764aff56625"
                 }
        response = requests.request("GET", url, headers=headers)
        # print(response.text)
        js = json.loads(response.text)
        print("******", js)
        result = js.get('data')

        return result

