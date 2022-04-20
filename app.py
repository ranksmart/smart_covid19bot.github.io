# doing necessary imports
from flask import Flask, render_template, request, make_response
from flask_cors import CORS, cross_origin
# import requests
# import pymongo
import json
import MakeApiRequests
import EMailClient
from indianstates import indianstate
# from pymongo import MongoClient

app = Flask(__name__)  # initialising the flask app with the name 'app'


# geting and sending response to dialogflow
@app.route('/', methods=['GET'])
def welcome():
    return"""
    <!DOCTYPE html>
<head>
   <title>Covid19</title>
</head>
<body>  
   <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
<df-messenger
  intent="WELCOME"
  chat-title="Covid19_Cases"
  agent-id="16f85c0e-f3bb-47e0-8883-7faf10beffd8"
  language-code="en"
></df-messenger>
</body>
    
    """

@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    # dbConn = pymongo.MongoClient("mongodb://localhost:27017/")  # opening a connection to Mongo
    # log = Conversations.Log()
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    query_text = result.get("queryText")
    parameters = result.get("parameters")
    cust_name = parameters.get("cust_name")
    cust_contact = parameters.get("cust_contact")
    cust_email = parameters.get("cust_email")
    # db = configureDataBase()
    global fulfill,country

    if intent == 'covid_searchcountry':
        cust_country = parameters.get("geo-country")
        if(cust_country=="United States"):
            cust_country = "USA"
        country=cust_country
        

        fulfillmentText, deaths_data, testsdone_data = makeAPIRequest(cust_country)
        fulfill=fulfillmentText
        webhookresponse = "***Covid Report*** \n\n" + " New cases :" + str(fulfillmentText.get('new')) + \
                          "\n" + " Active cases : " + str(
            fulfillmentText.get('active')) + "\n" + " Critical cases : " + str(fulfillmentText.get('critical')) + \
                          "\n" + " Recovered cases : " + str(
            fulfillmentText.get('recovered')) + "\n" + " Total cases : " + str(fulfillmentText.get('total')) + \
                          "\n" + " Total Deaths : " + str(deaths_data.get('total')) + "\n" + " New Deaths : " + str(
            deaths_data.get('new')) + \
                          "\n" + " Total Test Done : " + str(deaths_data.get('total')) + "\n\n*******END********* \n "

        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            webhookresponse
                        ]

                    }
                },
                {
                    "text": {
                        "text": [
                            "Do you want me to send the detailed report to your e-mail address? Type.. \n 1. Sure \n 2. Not now "
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                    }
                }
            ]
        }
    elif intent == "Welcome" or intent == "continue_conversation" or intent == "not_send_email" or intent == "endConversation" or intent == "Fallback" or intent == "covid_faq" or intent == "select_country_option":
        fulfillmentText = result.get("fulfillmentText")
        # log.saveConversations(sessionID, query_text, fulfillmentText, intent, db)
    elif intent == "send_report_to_email":
        fulfillmentText = result.get("fulfillmentText")
        # log.saveConversations(sessionID, "Sure send email", fulfillmentText, intent, db)
        # val = log.getcasesForEmail("country", "", db)
        # print("===>",val)
        print(fulfill.get("active"))
        prepareEmail([cust_name, cust_contact, cust_email,fulfill,country])

    elif intent == "totalnumber_cases":
        fulfillmentText = makeAPIRequest("world")
        webhookresponse = "***World wide Report*** \n\n" + " Confirmed cases :" + str(
            fulfillmentText.get('confirmed')) + \
                          "\n" + " Deaths cases : " + str(
            fulfillmentText.get('deaths')) + "\n" + " Recovered cases : " + str(fulfillmentText.get('recovered')) + \
                          "\n" + " Active cases : " + str(
            fulfillmentText.get('active')) + "\n" + " Fatality Rate : " + str(
            fulfillmentText.get('fatality_rate') * 100) + "%" + \
                          "\n" + " Last updated : " + str(
            fulfillmentText.get('last_update')) + "\n\n*******END********* \n "
        # # # print(webhookresponse)
        # log.saveConversations(sessionID, "Cases worldwide", webhookresponse, intent, db)
        # log.saveCases("world", fulfillmentText, db)

        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            webhookresponse
                        ]

                    }
                },
                {
                    "text": {
                        "text": [
                            "Do you want me to send the detailed report to your e-mail address? Type.. \n 1. Sure \n 2. Not now "
                            # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
                        ]

                    }
                }
            ]
        }

    elif intent == "indianstates":
        state=parameters.get("geo-state")
        fulfillmentText=indianstate(state)
        webhookresponse=f"***{state} covid_cases report*** \n\n" + " Active cases : " + str(
            fulfillmentText.get('active')) + \
                "\n" + " Recovered cases : " + str(
            fulfillmentText.get('recovered')) + "\n" + " Total cases : " + str(fulfillmentText.get('total')) + \
                          "\n" + " Total Deaths : " + str(fulfillmentText.get('Death')) 
        return {
            "fulfillmentMessages":[ 
                {
                    "text": {
                        "text": [
                            webhookresponse 
                            
                        ]

                    }
                }
            ]
        }


       

        # log.saveConversations(sessionID, "Indian State Cases", webhookresponse1, intent, db)
        
    else:
        return {
            "fulfillmentText": "something went wrong,Lets start from the begining, Say Hi",
        }


# def configureDataBase():
#     client = MongoClient("mongodb+srv://covid19:<rank>@cluster0.fjjxb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#     return client.get_database('covid')


def makeAPIRequest(query):
    api = MakeApiRequests.Api()

    if query == "world":
        return api.makeApiWorldwide()
    else:
        return api.makeApiRequestForCounrty(query)


def prepareEmail(contact_list):
    EMailClient.sendEmail(contact_list)


if __name__ == '__main__':
    # port = int(os.getenv('PORT'))
    # print("Starting app on port %d" % port)
    app.run(debug=False)
'''if __name__ == "__main__":
    app.run(port=5000, debug=True)''' # running the app on the local machine on port 8000
