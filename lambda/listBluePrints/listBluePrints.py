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

    resp = table.query(
        IndexName='latest',
        KeyConditionExpression=Key('version').eq('latest')
    )

    body = resp['Items']
    response = {
        "statusCode": '200',
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body, indent=4) 
    }

    print('Result: {}'.format(body))
    return response
