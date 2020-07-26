import os
import sys
import json
import logging
import requests
import azure.functions as func
from . import helpers
import time

formsRecognizerKey = os.environ["FormsRecognizerKey"]
formsRecognizerEndpoint = os.environ["FormsRecognizerEndpoint"]
modelId = os.environ["ModelId"]
# uri = f"https://{formsRecognizerEndpoint}/formrecognizer/v1.0-preview/custom/models/{modelId}/analyze"
uri = f"https://{formsRecognizerEndpoint}/formrecognizer/v2.0/custom/models/{modelId}/analyze"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoice Skill Request: Python HTTP trigger function processed a request.')
    
    # get request body
    body = req.get_json()

    # prep return shape
    records = { 'values': [] }

    for record in body["values"]:
        try:
            # get pdf form
            logging.info(f'requesting get url: {record["data"]["formUrl"]}{record["data"]["formSasToken"]}')
            pdf = requests.get(f'{record["data"]["formUrl"]}{record["data"]["formSasToken"]}')

            # make Form Recognizer API request
            logging.info(f'CogSvc Form Request: {uri}')
            response = requests.post(uri, data=pdf, headers={ 
                'Ocp-Apim-Subscription-Key': formsRecognizerKey,
                'Content-Type': 'application/pdf' })

            # logging.info(f'response full: {response}')
            headers = response.headers
            retLocation = headers['Operation-Location']
            logging.info(f'response headers: {headers}')

            logging.info(f'retrieve location: {retLocation}')

            time.sleep(10)
                
            retResponse = requests.get(retLocation, headers = { 'Ocp-Apim-Subscription-Key': formsRecognizerKey})
            # logging.info(f'Got retrieve response {retResponse.json()}')

            # cog_response = response.json()
            cog_response = retResponse.json()
            logging.info(f'CogSvc Form Response: {cog_response}')

            # Error from Cognitive Services?
            if 'error' in cog_response:
                code = cog_response['error']['code']
                message = cog_response['error']['message']
                logging.error(f'CogSvc Error {code}: {message}')
                records['values'].append({
                    'recordId': record["recordId"],
                    'data': {
                        'formUrl': record["data"]["formUrl"],
                        'invoice': {},
                        'error': {
                            'code': code,
                            'message': message,
                            'type': 'Cognitive Service Error'
                        }
                    }
                })
            else:
                logging.info('stuff is here...')
                #logging.info(f'readResults = {cog_response['analyzeResult']['readResults']}')
                records['values'].append({
                    'recordId': record["recordId"],
                    'data': {
                        'formUrl': record["data"]["formUrl"],
                        'invoice': helpers.convert(cog_response['analyzeResult']),
                        'error': {}
                    }
                })
        except Exception as error:
            logging.exception('Python Error')
            
            records['values'].append({
                'recordId': record["recordId"],
                'data': {
                    'formUrl': record["data"]["formUrl"],
                    'invoice': { },
                    'error': { 
                        'code': '500',
                        'message': f'{type(error).__name__}: {str(error)}',
                        'type': 'Python Error'
                    }
                }
            })

    return func.HttpResponse(body=json.dumps(records), 
                             headers={ 'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*" })
