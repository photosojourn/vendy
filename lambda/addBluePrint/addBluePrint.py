import json
import os

import boto3
from boto3.dynamodb.conditions import Key, Attr
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

ddb = boto3.resource('dynamodb')
tableName = os.environ['TABLE_NAME']
table = ddb.Table(tableName)


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    body = json.loads(event['body'])

    try:
        resp = table.update_item(
            Key={
                'blueprintName': body['blueprintname'],
                'version':'latest'
            },
            AttributeUpdates={
                'repoUrl': {
                    'Value': body['repourl'],
                    'Action': 'PUT'
                }
            }
        )

        response = {
            "statusCode": '200',
            "headers": {
                "Content-Type": "application/text",
            },
            "body": "200: Blueprint Updated."
        }


    except Exception as e:
        print(e)
        response = {
            "statusCode": '500',
            "headers": {
                "Content-Type": "application/text",
            },
            "body": "500: Blueprint Update Failed."
        }

    return response
