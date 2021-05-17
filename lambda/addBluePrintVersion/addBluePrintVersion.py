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
                'version': body['version']
            },
            AttributeUpdates={
                'status': {
                    'Value': 'ACTIVE',
                    'Action': 'PUT'
                },
                'repoURL': {
                    'Value': body['repourl'],
                    'Action': 'PUT'
                }
            }
        )
    except Exception as e:
        response = {
            "statusCode": '500',
            "headers": {
                "Content-Type": "application/text",
            },
            "body": "500: Adding Blueprint Version Failed."
        }

    else:
        try:
            print("Updating master")
            resp2 = table.update_item(
                  Key={
                      'blueprintName': body['blueprintname'],
                      'version': 'latest'
                  },
                  AttributeUpdates={
                      'latest': {
                          'Value': body['version'],
                          'Action': 'PUT'
                      }
                  }
            )

            print(resp2)

            response = {
                "statusCode": '200',
                "headers": {
                    "Content-Type": "application/text",
                },
                "body": "200: Blueprint Updated."
            }

        except Exception as e:
            response = {
                "statusCode": '500',
                "headers": {
                    "Content-Type": "application/text",
                },
                "body": "500: Update Master Blueprint Version Failed."
            }

    return response
