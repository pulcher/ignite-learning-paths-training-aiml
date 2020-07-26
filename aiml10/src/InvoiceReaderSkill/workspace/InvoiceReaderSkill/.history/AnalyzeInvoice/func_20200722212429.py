import os
import sys
import json
import logging
import requests
import azure.functions as func
from . import helpers

formsRecognizerKey = os.environ["FormsRecognizerKey"]
formsRecognizerEndpoint = os.environ["FormsRecognizerEndpoint"]
modelId = os.environ["ModelId"]
uri = f"https://{formsRecognizerEndpoint}/formrecognizer/v2.0/custom/models/{modelId}/analyze"
logging.debug(uri)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoice Skill Request: Python HTTP trigger function processed a request.')
    
    # get request body
    body = req.get_json()
    logging.info(f'request body: {body}')

    # prep return shape
    records = { 'values': [] }

    for record in body["values"]:
        try:
            # get pdf form
            logging.info(f'incoming request:')
            '{record["data"]["formUrl"]}{record["data"]["formSasToken"]}')
            pdf = requests.get(f'{record["data"]["formUrl"]}{record["data"]["formSasToken"]}')
            logging.info(f'pdf request: {pdf}')

            # make Form Recognizer API request
            logging.info(f'CogSvc Form Request: {uri}')
            response = requests.post(uri, data=pdf, headers={ 
                'Ocp-Apim-Subscription-Key': formsRecognizerKey,
                'Content-Type': 'application/pdf' })

            cog_response = response.json()
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
                records['values'].append({
                    'recordId': record["recordId"],
                    'data': {
                        'formUrl': record["data"]["formUrl"],
                        'invoice': helpers.convert(cog_response),
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
