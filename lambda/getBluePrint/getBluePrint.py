import json
import os

import boto3
import string
import logging
from boto3.dynamodb.conditions import Key, Attr
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
from urllib import parse

#Enable Xray
patch_all()

#Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ddb = boto3.resource('dynamodb')
tableName = os.environ['TABLE_NAME']
table = ddb.Table(tableName)


def handler(event, context):
    logger.info('## REQUEST')
    logger.info(json.dumps(event))

    params = parse.parse_qs(event["rawQueryString"])

    logger.info('## PARAMETERS')
    logger.info(dict(params))


    action = (params['action'][0]).lower()
    bluePrintName = params['name'][0].lower()

    if action == "get":

        if "version" in params:
            version = params['version'][0]
        else:
            version = 'latest'

        try:
            resp = table.get_item(
                Key = {
                    'blueprintName': bluePrintName,
                    'version': version
                },
            )
            body = resp['Item']
            response = {
                "statusCode": '200',
                "headers": {
                    "Content-Type": "application/json",
                },
                "body": json.dumps(body, indent=4)
            }
            print('Result: {}'.format(body))
        except:
            response = {
                "statusCode": '404',
                "headers": {
                    "Content-Type": "application/text",
                },
                "body": "404: Blueprint not found."
            }
    elif action == 'list':
        try:
            logger.info("Listing blueprints")
            resp = table.query(
                IndexName='latest',
                KeyConditionExpression=Key('version').ne('latest'),
                #FilterExpression=Key('blueprintName').eq(bluePrintName)
            )
            body = resp['Items']
            print(body)
            response = {
                "statusCode": '200',
                "headers": {
                    "Content-Type": "application/json",
                },
                "body": json.dumps(body, indent=4)
            }
            print('Result: {}'.format(body))
        except Exception as e:
            logger.debug(e)
            response = {
                "statusCode": '404',
                "headers": {
                    "Content-Type": "application/text",
                },
                "body": "404: Blueprint not found."
            } 
    else:
        response = {
                "statusCode": '404',
                "headers": {
                    "Content-Type": "application/text",
                },
                "body": "500: Invalid Action."
            }

    return response