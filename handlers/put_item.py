'''Put item'''

import json
import logging
import os

import boto3

log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
_logger = logging.getLogger(__name__)

# DynamoDB
DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
DDT = dynamodb.Table(DDB_TABLE_NAME)


def _get_body_from_event(event):
    '''Get data from event body'''
    return json.loads(event.get('body'))


def _put_item(item):
    '''Put record item'''
    DDT.put_item(
        TableName=DDB_TABLE_NAME,
        Item=item
    )


def handler(event, context):
    '''Function entry'''
    _logger.debug('Event received: {}'.format(json.dumps(event)))

    item = _get_body_from_event(event)
    _put_item(item)

    resp = {
        'statusCode': 201,
        'body': json.dumps({'success': True})
    }
    _logger.debug('Response: {}'.format(json.dumps(resp)))
    return resp

