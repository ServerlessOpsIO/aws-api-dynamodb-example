'''Put item'''

import json
import logging
import os

import boto3
from botocore.config import Config

log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
_logger = logging.getLogger(__name__)

# This is actually the default per:
# https://github.com/boto/botocore/blob/15ecfbc7ea23f81981ca65626ee166df130f64db/botocore/data/_retry.json#L119-L126
AWS_CONFIG = Config(retries={'max_attempts': 10})

# DynamoDB
DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
dynamodb = boto3.resource('dynamodb', config=AWS_CONFIG)
DDT = dynamodb.Table(DDB_TABLE_NAME)


def _put_item(item):
    '''Put record item'''
    DDT.put_item(
        TableName=DDB_TABLE_NAME,
        Item=item
    )


def handler(event, context):
    '''Function entry'''
    _logger.debug('Event received: {}'.format(json.dumps(event)))

    item = json.loads(event.get('body'))
    _put_item(item)

    resp = {
        'statusCode': 201,
        'body': json.dumps({'success': True})
    }
    _logger.debug('Response: {}'.format(json.dumps(resp)))
    return resp

