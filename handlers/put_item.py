'''Put item'''

import json
import logging
import os

import boto3
from botocore.config import Config
from tenacity import retry, stop_after_delay, wait_random_exponential

log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
_logger = logging.getLogger(__name__)

# Using tenacity instead
AWS_CONFIG = Config(retries={'max_attempts': 0})

# DynamoDB
DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
dynamodb = boto3.resource('dynamodb', config=AWS_CONFIG)
DDT = dynamodb.Table(DDB_TABLE_NAME)


@retry(wait=wait_random_exponential(), stop=stop_after_delay(28))
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

